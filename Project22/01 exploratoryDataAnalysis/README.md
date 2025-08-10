# Exploratory Data Analysis: AMD vs NVDA

## 📋 Project Description

This project performs a comprehensive exploratory data analysis (EDA) of AMD and NVDA stocks, two of the leading companies in the semiconductor sector, using historical price data from 2020 to 2025.

## 🎯 Objectives

- **Comparative Analysis**: Examine the temporal evolution of AMD and NVDA closing prices
- **Pattern Identification**: Detect trends, correlations, and seasonal behaviors
- **Data Visualization**: Create informative charts to facilitate data interpretation
- **Investment Insights**: Provide useful conclusions for investment decision-making

## 🛠️ Tools and Technologies

### Programming Languages
- **Python 3.x**: Main language for data analysis

### Libraries Used
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical operations and arrays
- **yfinance**: Download financial data from Yahoo Finance
- **matplotlib**: Chart creation and visualizations
- **seaborn**: Advanced statistical visualizations

### Development Environment
- **Jupyter Notebook**: Interactive environment for data analysis
- **VS Code**: Code editor with notebook support

## 📊 Types of Analysis Performed

### 1. Temporal Analysis
- **Line charts**: Evolution of closing prices over time
- **Direct comparison**: AMD vs NVDA in the same period

### 2. Correlation Analysis
- **Scatter plots**: Relationship between closing prices of both stocks
- **Temporal correlation**: Year-by-year analysis using color coding

### 3. Distribution Analysis
- **Histograms**: Frequency distribution of closing prices
- **Pairplots**: Comparison of distributions and multiple relationships

### 4. Statistical Analysis
- **Descriptive statistics**: Mean, median, standard deviation, etc.
- **Missing value detection**: Data integrity verification

## 📁 Project Structure

```
Project22/
│
├── exploratoryDataAnalysis.ipynb    # Main notebook with the analysis
├── requirements.txt                 # Requirements
└── README.md                        # This file
```

## 🚀 How to Run the Project

### Prerequisites
```bash
pip install -r requirements.txt
```

### Execution
1. Clone or download the project
2. Open the `exploratoryDataAnalysis.ipynb` file in Jupyter Notebook or VS Code
3. Execute the cells sequentially

## 📈 Key Findings

### Strong Positive Correlation
AMD and NVDA show significant positive correlation, indicating that both stocks tend to move in the same direction.

### Volatility Differences
- **NVDA**: Higher volatility and more dramatic growth
- **AMD**: More stable behavior with consistent growth

### Temporal Patterns
The data reveals distinct patterns by year, especially during periods of high technological demand (AI boom, chip shortage, etc.).

## 🎯 Conclusions and Recommendations

### For Investors
- **Diversification**: High correlation suggests limited diversification benefits between these two stocks
- **Risk Profile**: NVDA for investors with higher risk tolerance, AMD for more conservative approaches
- **Sector Exposure**: Both stocks serve as excellent proxies for the semiconductor sector

### For Future Analysis
- Incorporate trading volume analysis
- Include additional technical indicators
- Perform market sentiment analysis

## 🔄 Next Steps

1. **Technical Analysis**: Implement indicators like RSI, MACD, Bollinger Bands
2. **Predictive Modeling**: Develop price prediction models
3. **Fundamental Analysis**: Incorporate companies' financial data
4. **Backtesting**: Test trading strategies based on findings


**Note**: This analysis is for educational purposes only and does not constitute financial advice. Always consult with a professional before making investment decisions.
