# FMCG Sales Data Preprocessing
## Persiapan Data untuk Google Looker

---

## TUJUAN NOTEBOOK

Persiapkan dan transformasikan dataset penjualan FMCG (1.1M baris, 33 kolom) untuk menghasilkan:

1. **Revenue Analysis**: Total penjualan (net_sales) per negara
2. **SKU Performance**: Top 20 SKU berdasarkan revenue
3. **ABC Classification**: Perbandingan kelas ABC (by revenue) per region/country
4. **XYZ Classification**: Identifikasi volatilitas per SKU (Coefficient of Variation pada units_sold)
5. **Correlation Analysis**: Korelasi antara harga (list_price), promosi (promo_flag, discount_pct), dan volume penjualan (units_sold)
6. **Seasonality Patterns**: Visualisasi pola musiman (monthly & weekly trends)

---

## EKSPEKTASI BISNIS / INSIGHT YANG DICARI

| Aspek | Ekspektasi |
|-------|------------|
| **Pola Musiman** | Puncak penjualan yang jelas terlihat (misalnya puncak musim panas/dingin tergantung kategori produk) |
| **Channel Comparison** | E-commerce menunjukkan volatilitas lebih tinggi dibanding channel fisik |
| **Promo Dependency** | Beberapa SKU teridentifikasi bergantung pada promosi (tinggi promo_lift) |
| **Regional Performance** | Identifikasi region berkinerja rendah yang mungkin memerlukan kebijakan safety-stock berbeda |
| **ABC-XYZ Matrix** | Kombinasi klasifikasi untuk strategi inventory optimal |

---

## OUTPUT YANG DIHARAPKAN

### 1. Aggregated Tables
| Tabel | Deskripsi |
|-------|----------|
| `agg_revenue_by_country` | Total revenue, units, avg_price per negara |
| `agg_revenue_by_sku` | Revenue, units, avg_price, ABC class per SKU |
| `agg_monthly_trend` | Aggregasi bulanan untuk analisis musiman |
| `agg_weekly_trend` | Aggregasi mingguan untuk pola weekday |

### 2. Lookup/Dimension Tables
| Tabel | Deskripsi |
|-------|----------|
| `dim_sku` | SKU ID, name, category, subcategory, brand |
| `dim_store` | Store ID, country, city, channel, coordinates |
| `dim_supplier` | Supplier ID, lead_time_days, purchase_cost |

### 3. Metrik yang Terdefinisi
```
• revenue = SUM(net_sales)
• units = SUM(units_sold)
• avg_price = AVG(list_price)
• promo_lift = (Revenue dengan Promo / Revenue tanpa Promo) - 1
• CV (Coefficient of Variation) = STD(units) / MEAN(units) → untuk XYZ class
• ABC class: A (top 80%), B (next 15%), C (bottom 5%)
• XYZ class: X (CV < 0.5), Y (0.5 ≤ CV < 1), Z (CV ≥ 1)
```

### 4. Artifacts Preprocessing
- File Parquet terpartisi untuk efisiensi query
- Summary statistics untuk validasi

### 5. Visualisasi Validasi (Matplotlib)
- Trend bulanan revenue
- Heatmap korelasi
- Bar chart ABC per region
- Scatter plot promo vs sales
