"""
Script untuk memperbaiki file CSV agar kompatibel dengan Google Looker & Google Sheets.

Perbaikan yang dilakukan:
1. Menambahkan kolom identifier pada file yang tidak memilikinya
2. Menghapus baris kosong di akhir file
3. Mengonversi line endings ke format standar (Unix LF)
4. Membersihkan nama kolom (snake_case, tanpa karakter khusus)
5. Memformat angka dengan konsisten (2 desimal untuk persentase, integer untuk count)
6. Menghapus spasi berlebih di data
7. Menggunakan UTF-8 encoding dengan BOM untuk kompatibilitas maksimal
8. Menyimpan file yang sudah diperbaiki ke folder baru

Author: Nandana Ayudya Natasaskara
Date: 2025-12-08
"""

import os
import re
import pandas as pd
import numpy as np
from pathlib import Path


def clean_column_name(col_name: str) -> str:
    """
    Membersihkan nama kolom agar kompatibel dengan Google Sheets/Looker.
    
    Args:
        col_name: Nama kolom asli
    
    Returns:
        Nama kolom yang sudah dibersihkan (snake_case)
    """
    # Hapus spasi di awal/akhir
    cleaned = col_name.strip()
    
    # Ganti spasi dan karakter khusus dengan underscore
    cleaned = re.sub(r'[^\w\s]', '_', cleaned)
    cleaned = re.sub(r'\s+', '_', cleaned)
    
    # Hapus underscore berlebih
    cleaned = re.sub(r'_+', '_', cleaned)
    
    # Hapus underscore di awal/akhir
    cleaned = cleaned.strip('_')
    
    # Lowercase untuk konsistensi
    cleaned = cleaned.lower()
    
    return cleaned


def format_numeric_value(value, col_name: str, is_correlation: bool = False):
    """
    Memformat nilai numerik berdasarkan tipe kolom.
    
    Args:
        value: Nilai yang akan diformat
        col_name: Nama kolom untuk menentukan format
        is_correlation: True jika file adalah correlation matrix
    
    Returns:
        Nilai yang sudah diformat
    """
    if pd.isna(value):
        return ''
    
    # Untuk correlation matrix, selalu gunakan format float dengan 2-3 desimal
    if is_correlation:
        if isinstance(value, (int, float)):
            return round(value, 3)  # Presisi 3 desimal untuk korelasi
        return value
    
    # Kolom yang seharusnya integer (hanya untuk non-correlation files)
    # Gunakan exact match untuk menghindari false positive
    integer_columns = ['count', 'rows', 'columns', 'sku_count', 'transaction_count']
    
    # Kolom persentase (format 2 desimal)
    percentage_columns = ['pct', 'percentage', 'margin', 'cv']
    
    # Kolom revenue/price (format 2 desimal)
    money_columns = ['revenue', 'price', 'sales', 'cost']
    
    col_lower = col_name.lower()
    
    if isinstance(value, (int, float)):
        # Cek apakah kolom integer - gunakan exact match di akhir nama kolom
        if any(col_lower.endswith(term) or col_lower == term for term in integer_columns):
            return int(value) if not pd.isna(value) else ''
        # Cek apakah kolom persentase atau uang
        elif any(term in col_lower for term in percentage_columns + money_columns):
            return round(value, 2)
    
    return value


def fix_csv_files(input_folder: str, output_folder: str) -> dict:
    """
    Memperbaiki semua file CSV dalam folder input dan menyimpannya ke folder output.
    Format output dioptimalkan untuk Google Sheets dan Looker.
    
    Args:
        input_folder: Path ke folder yang berisi file CSV asli
        output_folder: Path ke folder untuk menyimpan file CSV yang sudah diperbaiki
    
    Returns:
        Dictionary berisi status perbaikan untuk setiap file
    """
    
    # Buat folder output jika belum ada
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    input_path = Path(input_folder)
    results = {}
    
    # Daftar file yang memerlukan kolom identifier khusus
    identifier_mapping = {
        'abc_summary.csv': {'column_name': 'abc_class', 'values': ['A', 'B', 'C']},
        'xyz_summary.csv': {'column_name': 'xyz_class', 'values': ['X']},
        'promo_analysis.csv': {'column_name': 'promo_flag', 'values': [0, 1]},
        'correlation_matrix.csv': {
            'column_name': 'variable', 
            'values': ['list_price', 'discount_pct', 'promo_flag', 'units_sold', 
                      'net_sales', 'gross_sales', 'margin_pct']
        },
    }
    
    # Proses setiap file CSV
    for csv_file in input_path.glob('*.csv'):
        filename = csv_file.name
        fixes_applied = []
        
        try:
            # Baca file CSV dengan encoding yang fleksibel
            try:
                df = pd.read_csv(csv_file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(csv_file, encoding='latin-1')
                fixes_applied.append("Fixed encoding (latin-1 to UTF-8)")
            
            original_rows = len(df)
            original_cols = list(df.columns)
            
            # 1. Hapus baris kosong (baris dengan semua nilai NaN)
            df = df.dropna(how='all')
            if len(df) < original_rows:
                fixes_applied.append(f"Removed {original_rows - len(df)} empty rows")
            
            # 2. Bersihkan nama kolom
            new_columns = [clean_column_name(col) for col in df.columns]
            if new_columns != list(df.columns):
                df.columns = new_columns
                fixes_applied.append("Cleaned column names (snake_case)")
            
            # 3. Tambahkan kolom identifier jika diperlukan
            if filename in identifier_mapping:
                mapping = identifier_mapping[filename]
                col_name = mapping['column_name']
                values = mapping['values']
                
                # Hanya tambahkan jika kolom belum ada
                if col_name not in df.columns:
                    if len(values) == len(df):
                        df.insert(0, col_name, values)
                        fixes_applied.append(f"Added identifier column '{col_name}'")
                    else:
                        df.insert(0, col_name, range(1, len(df) + 1))
                        fixes_applied.append(f"Added identifier column '{col_name}' (auto-numbered)")
            
            # 4. Bersihkan spasi di data string
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
            fixes_applied.append("Trimmed whitespace in text columns")
            
            # 5. Format nilai numerik
            # Deteksi apakah ini correlation matrix untuk mempertahankan presisi
            is_correlation = 'correlation' in filename.lower()
            for col in df.select_dtypes(include=['float64', 'int64']).columns:
                df[col] = df[col].apply(lambda x: format_numeric_value(x, col, is_correlation))
            fixes_applied.append("Standardized numeric formatting")
            
            # 6. Ganti NaN dengan string kosong untuk kompatibilitas Sheets
            df = df.fillna('')
            fixes_applied.append("Replaced NaN with empty strings")
            
            # 7. Simpan ke folder output dengan format Google Sheets-ready
            output_file = output_path / filename
            
            # Gunakan UTF-8 dengan BOM untuk kompatibilitas maksimal
            df.to_csv(
                output_file, 
                index=False, 
                encoding='utf-8-sig',  # UTF-8 dengan BOM
                lineterminator='\n',   # Unix line endings
                quoting=1,             # Quote semua field non-numerik
                float_format='%.2f'    # Format float dengan 2 desimal
            )
            fixes_applied.append("Saved with UTF-8 BOM encoding")
            fixes_applied.append("Applied Unix line endings (LF)")
            
            results[filename] = {
                'status': 'success',
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'fixes': fixes_applied
            }
            
        except Exception as e:
            results[filename] = {
                'status': 'error',
                'error': str(e)
            }
    
    return results


def generate_summary_report(results: dict, output_folder: str) -> None:
    """
    Generate laporan ringkasan perbaikan.
    
    Args:
        results: Dictionary hasil perbaikan dari fix_csv_files
        output_folder: Path folder output untuk menyimpan laporan
    """
    
    report_lines = [
        "=" * 70,
        "LAPORAN PERBAIKAN FILE CSV - GOOGLE SHEETS/LOOKER READY",
        "=" * 70,
        ""
    ]
    
    success_count = sum(1 for r in results.values() if r['status'] == 'success')
    error_count = sum(1 for r in results.values() if r['status'] == 'error')
    
    report_lines.append(f"Total file diproses: {len(results)}")
    report_lines.append(f"Berhasil: {success_count}")
    report_lines.append(f"Gagal: {error_count}")
    report_lines.append("")
    report_lines.append("-" * 70)
    report_lines.append("DETAIL PERBAIKAN")
    report_lines.append("-" * 70)
    
    for filename, result in results.items():
        report_lines.append(f"\n[FILE] {filename}")
        if result['status'] == 'success':
            report_lines.append(f"   Status: [OK] Berhasil")
            report_lines.append(f"   Baris: {result['rows']}, Kolom: {result['columns']}")
            report_lines.append(f"   Nama Kolom: {', '.join(result['column_names'][:5])}...")
            report_lines.append(f"   Perbaikan yang diterapkan:")
            for fix in result['fixes']:
                report_lines.append(f"     - {fix}")
        else:
            report_lines.append(f"   Status: [ERROR] Gagal")
            report_lines.append(f"   Error: {result['error']}")
    
    report_lines.append("")
    report_lines.append("=" * 70)
    report_lines.append("LANGKAH SELANJUTNYA:")
    report_lines.append("  1. Buka Google Drive (drive.google.com)")
    report_lines.append("  2. Upload semua file CSV dari folder output")
    report_lines.append("  3. Klik kanan pada file -> 'Open with' -> 'Google Sheets'")
    report_lines.append("  4. Di Looker, pilih 'Google Sheets' sebagai data source")
    report_lines.append("=" * 70)
    report_lines.append(f"\nFile output: {output_folder}")
    
    # Print ke console
    print("\n".join(report_lines))
    
    # Simpan ke file
    report_path = Path(output_folder) / "_fix_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))


def generate_looker_schema(results: dict, output_folder: str) -> None:
    """
    Generate file schema untuk membantu konfigurasi di Looker.
    
    Args:
        results: Dictionary hasil perbaikan dari fix_csv_files
        output_folder: Path folder output
    """
    
    schema_lines = [
        "# Schema Reference untuk Google Looker",
        "# File ini berisi daftar kolom untuk setiap tabel",
        "# Gunakan sebagai referensi saat membuat data model di Looker",
        "",
        "=" * 60,
        ""
    ]
    
    for filename, result in results.items():
        if result['status'] == 'success':
            schema_lines.append(f"## {filename}")
            schema_lines.append(f"Rows: {result['rows']} | Columns: {result['columns']}")
            schema_lines.append("")
            schema_lines.append("| Column Name | Type (suggested) |")
            schema_lines.append("|-------------|-----------------|")
            
            for col in result['column_names']:
                # Suggest type based on column name
                col_lower = col.lower()
                if any(x in col_lower for x in ['id', 'flag', 'count', 'units', 'rows']):
                    dtype = "INTEGER"
                elif any(x in col_lower for x in ['pct', 'percentage', 'margin', 'cv']):
                    dtype = "FLOAT (percentage)"
                elif any(x in col_lower for x in ['revenue', 'price', 'sales', 'cost']):
                    dtype = "FLOAT (currency)"
                elif any(x in col_lower for x in ['date', 'month', 'week', 'year']):
                    dtype = "DATE/STRING"
                elif any(x in col_lower for x in ['name', 'class', 'category', 'brand']):
                    dtype = "STRING"
                else:
                    dtype = "STRING/FLOAT"
                
                schema_lines.append(f"| {col} | {dtype} |")
            
            schema_lines.append("")
            schema_lines.append("-" * 60)
            schema_lines.append("")
    
    # Simpan ke file
    schema_path = Path(output_folder) / "_schema_reference.md"
    with open(schema_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(schema_lines))
    
    print(f"\n[INFO] Schema reference saved to: {schema_path}")


def main():
    """
    Fungsi utama untuk menjalankan perbaikan CSV.
    """
    
    # Tentukan path folder
    script_dir = Path(__file__).parent
    input_folder = script_dir / "output_looker"
    output_folder = script_dir / "output_looker_sheets_ready"
    
    print("=" * 70)
    print("CSV FIXER FOR GOOGLE SHEETS & LOOKER")
    print("=" * 70)
    print(f"\nInput folder : {input_folder}")
    print(f"Output folder: {output_folder}")
    print("\nPerbaikan yang akan dilakukan:")
    print("  - Menambahkan kolom identifier")
    print("  - Membersihkan nama kolom (snake_case)")
    print("  - Memformat angka dengan konsisten")
    print("  - Menghapus baris kosong")
    print("  - Konversi ke UTF-8 dengan BOM")
    print("  - Unix line endings")
    print("\nMemproses file...")
    
    # Jalankan perbaikan
    results = fix_csv_files(str(input_folder), str(output_folder))
    
    # Generate laporan
    generate_summary_report(results, str(output_folder))
    
    # Generate schema reference
    generate_looker_schema(results, str(output_folder))
    
    print("\n[DONE] Selesai! File CSV siap diupload ke Google Sheets/Looker.")


if __name__ == "__main__":
    main()
