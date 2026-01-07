# FMCG Sales Data Preprocessing Pipeline

## Project Overview

This project implements a comprehensive data preprocessing pipeline for **Fast-Moving Consumer Goods (FMCG) sales data** from the Kaggle dataset `fmcg-multi-country-sales-dataset`. The preprocessing transforms raw sales transactions into analytics-ready outputs optimized for **Google Looker Studio** dashboards.

### Dataset Source
- **Source**: [Kaggle - FMCG Multi-Country Sales Dataset](https://www.kaggle.com/datasets/robertocarlost/fmcg-multi-country-sales-dataset)
- **Original File**: `fmcg_sales_3years_1M_rows.csv` (~1 million rows of 3-year sales data)

---

## Objectives

| Objective | Description |
|-----------|-------------|
| **Data Preparation** | Clean and transform raw sales data for business intelligence |
| **Inventory Classification** | Implement ABC-XYZ analysis for SKU prioritization |
| **Promo Impact Analysis** | Measure promotion effectiveness using promo_lift metrics |
| **Regional Insights** | Aggregate performance by country and region |
| **Looker Integration** | Export data in optimized CSV formats for dashboard consumption |

---

## Key Business Insights

| Insight Area | Finding |
|--------------|---------|
| **Total Revenue** | ~$473 million across 7 European countries |
| **Top Market** | Italy leads with $137M revenue (29% of total) |
| **SKU Portfolio** | 102 unique SKUs across 6 categories |
| **Promo Effectiveness** | Promotions increase units/transaction from 55 → 104 (89% lift) |
| **Demand Stability** | All 102 SKUs classified as "X" (CV < 0.5) - indicating stable demand |

---

## Methodology

### 1. ABC Classification
Revenue-based product classification using Pareto principle:

| Class | Criteria | SKU Count | Revenue Share |
|-------|----------|-----------|---------------|
| **A** (High Value) | Top 80% revenue | 49 SKUs | 79.42% |
| **B** (Medium Value) | Next 15% revenue | 29 SKUs | 15.57% |
| **C** (Low Value) | Bottom 5% revenue | 24 SKUs | 5.01% |

### 2. XYZ Classification
Demand variability classification using Coefficient of Variation (CV):

| Class | CV Threshold | Interpretation |
|-------|--------------|----------------|
| **X** | CV < 0.5 | Stable, predictable demand |
| **Y** | 0.5 ≤ CV < 1.0 | Moderate variability |
| **Z** | CV ≥ 1.0 | Highly unpredictable |

### 3. Key Formulas

```
• Revenue = units_sold × list_price × (1 - discount_pct)
• Promo Lift = (Revenue with Promo / Revenue without Promo) - 1
• CV (Coefficient of Variation) = STD(units) / MEAN(units)
```

---

## 📁 Output Files

All processed files are exported to `output_looker/` directory:

### Dimension Tables (Master Data)
| File | Description | Rows |
|------|-------------|------|
| `dim_sku.csv` | Complete SKU master with ABC-XYZ classification | 102 |
| `dim_store.csv` | Store/channel dimension table | 13 |
| `dim_supplier.csv` | Supplier dimension table | 60 |

### Fact Tables (Aggregated Metrics)
| File | Description | Rows |
|------|-------------|------|
| `agg_revenue_by_country.csv` | Revenue by country | 7 |
| `agg_monthly_trend.csv` | Monthly sales trends | 36 |
| `agg_weekly_trend.csv` | Weekly performance summary | 7 |
| `sku_revenue.csv` | SKU-level revenue metrics | 102 |
| `top_20_sku.csv` | Top 20 SKUs by revenue (Pareto chart) | 20 |

### Analysis Tables
| File | Description | Rows |
|------|-------------|------|
| `abc_df.csv` | Detailed ABC classification | 102 |
| `abc_summary.csv` | ABC class summary | 3 |
| `abc_by_region.csv` | ABC breakdown by region | 21 |
| `xyz_df.csv` | Detailed XYZ classification | 102 |
| `xyz_summary.csv` | XYZ class summary | 1 |
| `promo_analysis.csv` | Promo vs non-promo comparison | 2 |
| `promo_lift_by_cat.csv` | Promo lift by category | 5 |
| `correlation_matrix.csv` | Feature correlations | 7 |

### Visualization Assets
| File | Description |
|------|-------------|
| `validation_dashboard.png` | Matplotlib validation charts |

---

## 🌍 Data Coverage

### Countries
| Country | Revenue | % of Total |
|---------|---------|------------|
| Italy | $137.2M | 29.0% |
| Spain | $106.7M | 22.6% |
| Germany | $88.5M | 18.7% |
| Austria | $43.0M | 9.1% |
| France | $42.6M | 9.0% |
| Poland | $42.4M | 9.0% |
| Netherlands | $12.5M | 2.6% |

### Product Categories
- 🥤 **Beverages** (Soda, Juice, Water, Energy drink)
- 🍪 **Snacks** (Chips, Chocolate, Biscuits, Nuts)
- 🧀 **Dairy** (Milk, Cheese, Yogurt)
- 🧼 **Home Care** (Detergent, Softener, Cleaner)
- 🧴 **Personal Care** (Soap, Shampoo, Toothpaste)

### Brands
6 major brands: BrandA, BrandB, BrandC, BrandD, BrandE, BrandF

---

## 🔧 Technical Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.14 |
| **Notebook** | Jupyter Notebook |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib |
| **Data Download** | KaggleHub |
| **Output Format** | CSV (Looker-compatible) |

---

## 📈 Usage with Google Looker Studio

1. **Upload CSV files** to Google Cloud Storage or BigQuery
2. **Create data sources** in Looker Studio for each table
3. **Join tables** using:
   - `sku_id` → connects SKU tables
   - `country` → connects geographic tables
   - `category` → connects product dimensions

### Recommended Dashboard Views
- **Executive Summary**: Revenue by country, monthly trends
- **Inventory Matrix**: ABC-XYZ scatter plot
- **Promo Effectiveness**: Before/after promo comparison
- **SKU Performance**: Top 20 Pareto chart

---

## 📂 Project Structure

```
preprocessing-data-fmcg/
├── preprocessing-data-3.ipynb   # Main notebook
├── EXPLAIN.md                   # This documentation
├── output_looker/               # Processed CSV outputs
│   ├── dim_*.csv                # Dimension tables
│   ├── agg_*.csv                # Aggregated facts
│   ├── abc_*.csv                # ABC analysis
│   ├── xyz_*.csv                # XYZ analysis
│   ├── promo_*.csv              # Promotion analysis
│   └── validation_dashboard.png # Validation charts
└── dokum/                       # Additional documentation
```

---

## 👨‍💻 Author

*This preprocessing pipeline was developed as part of UAS (Ujian Akhir Semester) project for data analytics coursework.*
