# Lumber Price Research

Research project focused on **softwood lumber prices and futures**.

## Motivation

Lumber is a uniquely interesting commodity:
- Highly sensitive to housing starts, interest rates, and weather
- Experienced extreme volatility during 2020–2022
- Has both physical (Random Lengths) and futures (CME Lumber) markets
- Strong seasonal patterns and supply-side constraints (mills, logging, transportation)

## Research Directions

1. **Price & Volatility Dynamics**  
   Historical behavior of CME Lumber futures and cash prices

2. **Macro & Housing Linkages**  
   Relationship with housing starts, mortgage rates, building permits

3. **Technical & Quantitative Factors**  
   Moving averages, regime detection, seasonality, volatility forecasting

4. **Alternative Data** (future)  
   Weather, mill capacity, inventory reports, sentiment

## Repository Structure

```
lumber-price-research/
├── README.md
├── data/                  # Raw & processed data (gitignored)
├── notebooks/             # Exploratory analysis
├── research/
│   └── factors/           # Numbered factor modules
│       └── 01_baseline/   # First baseline analysis
└── src/                   # Reusable utilities
```

## Data Sources

| Source              | Ticker / Series          | Notes                          |
|---------------------|--------------------------|--------------------------------|
| CME Lumber Futures  | `LBR=F` (Yahoo)          | Continuous front-month         |
| Random Lengths      | Cash price indices       | Industry benchmark             |
| FRED                | Housing starts, rates    | Macro drivers                  |
| NOAA / Weather      | Precipitation, temp      | Supply disruptions             |

## Quick Start

```bash
git clone https://github.com/Liam-Son/lumber-price-research.git
cd lumber-price-research
pip install -r requirements.txt
```

## License

MIT
