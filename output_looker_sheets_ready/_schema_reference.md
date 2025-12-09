# Schema Reference untuk Google Looker
# File ini berisi daftar kolom untuk setiap tabel
# Gunakan sebagai referensi saat membuat data model di Looker

============================================================

## abc_by_region.csv
Rows: 21 | Columns: 7

| Column Name | Type (suggested) |
|-------------|-----------------|
| country | INTEGER |
| abc_class | STRING |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| transaction_count | INTEGER |
| unique_skus | STRING/FLOAT |
| revenue_pct | FLOAT (percentage) |

------------------------------------------------------------

## abc_df.csv
Rows: 102 | Columns: 11

| Column Name | Type (suggested) |
|-------------|-----------------|
| sku_id | INTEGER |
| sku_name | STRING |
| category | STRING |
| brand | STRING |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| avg_price | FLOAT (currency) |
| transaction_count | INTEGER |
| revenue_pct | FLOAT (percentage) |
| cumulative_pct | FLOAT (percentage) |
| abc_class | STRING |

------------------------------------------------------------

## abc_summary.csv
Rows: 3 | Columns: 6

| Column Name | Type (suggested) |
|-------------|-----------------|
| abc_class | STRING |
| sku_count | INTEGER |
| total_revenue | FLOAT (currency) |
| avg_revenue | FLOAT (currency) |
| pct_sku | FLOAT (percentage) |
| pct_revenue | FLOAT (percentage) |

------------------------------------------------------------

## agg_monthly_trend.csv
Rows: 36 | Columns: 8

| Column Name | Type (suggested) |
|-------------|-----------------|
| year | DATE/STRING |
| month | DATE/STRING |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| avg_price | FLOAT (currency) |
| transaction_count | INTEGER |
| promo_rate | STRING/FLOAT |
| year_month_label | DATE/STRING |

------------------------------------------------------------

## agg_revenue_by_country.csv
Rows: 7 | Columns: 6

| Column Name | Type (suggested) |
|-------------|-----------------|
| country | INTEGER |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| avg_price | FLOAT (currency) |
| transaction_count | INTEGER |
| avg_revenue_per_transaction | FLOAT (currency) |

------------------------------------------------------------

## agg_weekly_trend.csv
Rows: 7 | Columns: 8

| Column Name | Type (suggested) |
|-------------|-----------------|
| weekday | DATE/STRING |
| weekday_name | DATE/STRING |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| avg_revenue | FLOAT (currency) |
| avg_units | INTEGER |
| transaction_count | INTEGER |
| revenue_index | FLOAT (currency) |

------------------------------------------------------------

## correlation_matrix.csv
Rows: 7 | Columns: 8

| Column Name | Type (suggested) |
|-------------|-----------------|
| variable | STRING/FLOAT |
| list_price | FLOAT (currency) |
| discount_pct | INTEGER |
| promo_flag | INTEGER |
| units_sold | INTEGER |
| net_sales | FLOAT (currency) |
| gross_sales | FLOAT (currency) |
| margin_pct | FLOAT (percentage) |

------------------------------------------------------------

## dim_sku.csv
Rows: 102 | Columns: 12

| Column Name | Type (suggested) |
|-------------|-----------------|
| sku_id | INTEGER |
| sku_name | STRING |
| category | STRING |
| subcategory | STRING |
| brand | STRING |
| abc_class | STRING |
| total_revenue | FLOAT (currency) |
| revenue_pct | FLOAT (percentage) |
| xyz_class | STRING |
| cv | FLOAT (percentage) |
| mean_units | INTEGER |
| abc_xyz_class | STRING |

------------------------------------------------------------

## dim_store.csv
Rows: 13 | Columns: 11

| Column Name | Type (suggested) |
|-------------|-----------------|
| store_id | INTEGER |
| country | INTEGER |
| city | STRING/FLOAT |
| channel | STRING/FLOAT |
| latitude | STRING/FLOAT |
| longitude | STRING/FLOAT |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| transaction_count | INTEGER |
| avg_basket_size | STRING/FLOAT |
| unique_skus | STRING/FLOAT |

------------------------------------------------------------

## dim_supplier.csv
Rows: 60 | Columns: 12

| Column Name | Type (suggested) |
|-------------|-----------------|
| supplier_id | INTEGER |
| avg_lead_time | STRING/FLOAT |
| min_lead_time | STRING/FLOAT |
| max_lead_time | STRING/FLOAT |
| avg_purchase_cost | FLOAT (currency) |
| total_purchase_cost | FLOAT (currency) |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| unique_skus | STRING/FLOAT |
| transaction_count | INTEGER |
| avg_margin | FLOAT (percentage) |
| revenue_per_sku | FLOAT (currency) |

------------------------------------------------------------

## promo_analysis.csv
Rows: 2 | Columns: 7

| Column Name | Type (suggested) |
|-------------|-----------------|
| promo_flag | INTEGER |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| avg_units_per_transaction | INTEGER |
| avg_revenue_per_transaction | FLOAT (currency) |
| transaction_count | INTEGER |
| avg_discount | INTEGER |

------------------------------------------------------------

## promo_lift_by_cat.csv
Rows: 5 | Columns: 6

| Column Name | Type (suggested) |
|-------------|-----------------|
| revenue_no_promo | FLOAT (currency) |
| revenue_with_promo | FLOAT (currency) |
| units_no_promo | INTEGER |
| units_with_promo | INTEGER |
| revenue_lift | FLOAT (currency) |
| units_lift | INTEGER |

------------------------------------------------------------

## sku_revenue.csv
Rows: 102 | Columns: 8

| Column Name | Type (suggested) |
|-------------|-----------------|
| sku_id | INTEGER |
| sku_name | STRING |
| category | STRING |
| brand | STRING |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| avg_price | FLOAT (currency) |
| transaction_count | INTEGER |

------------------------------------------------------------

## top_20_sku.csv
Rows: 20 | Columns: 10

| Column Name | Type (suggested) |
|-------------|-----------------|
| sku_id | INTEGER |
| sku_name | STRING |
| category | STRING |
| brand | STRING |
| total_revenue | FLOAT (currency) |
| total_units | INTEGER |
| avg_price | FLOAT (currency) |
| transaction_count | INTEGER |
| pct_of_total | FLOAT (percentage) |
| cumulative_pct | FLOAT (percentage) |

------------------------------------------------------------

## xyz_df.csv
Rows: 102 | Columns: 9

| Column Name | Type (suggested) |
|-------------|-----------------|
| sku_id | INTEGER |
| mean_units | INTEGER |
| std_units | INTEGER |
| months_active | DATE/STRING |
| cv | FLOAT (percentage) |
| xyz_class | STRING |
| sku_name | STRING |
| category | STRING |
| brand | STRING |

------------------------------------------------------------

## xyz_summary.csv
Rows: 1 | Columns: 5

| Column Name | Type (suggested) |
|-------------|-----------------|
| xyz_class | STRING |
| sku_count | INTEGER |
| avg_cv | FLOAT (percentage) |
| avg_monthly_units | INTEGER |
| pct_sku | FLOAT (percentage) |

------------------------------------------------------------

## _export_summary.csv
Rows: 16 | Columns: 4

| Column Name | Type (suggested) |
|-------------|-----------------|
| table_name | STRING |
| rows | INTEGER |
| columns | STRING/FLOAT |
| file_size_kb | STRING/FLOAT |

------------------------------------------------------------
