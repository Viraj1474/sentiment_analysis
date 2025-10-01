# 🚀 Futuristic App Analytics Dashboard

**Interactive Futuristic App Analytics Dashboard built with Streamlit for analyzing Google Play apps.**

---

## Project Overview
This dashboard helps explore and analyze apps using **Ratings, Reviews**, and derived metrics. It includes **advanced KPIs**, interactive charts, and filters to visualize app performance, engagement, and sentiment trends.

Key futuristic features:
- **Performance Score**: Combines rating and sentiment to highlight top apps.
- **Hidden Gem Score**: Identifies underrated apps with strong potential.
- **Interactive Leaderboard**: Sparkline trends for app ratings.
- **Sentiment Distribution**: Pie chart showing Positive, Neutral, and Negative sentiments.
- **App Comparison**: Compare multiple apps’ rating trends.
- **CSV Download**: Export filtered data for further analysis.

---

## Features
- **Interactive KPI Cards** with light/dark themes
- **Leaderboard & Hidden Gems** with conditional formatting
- **Category Radar Chart** for app insights
- **Sentiment Pie Chart**
- **App Comparison Trend Charts**
- **Downloadable Filtered Data**

---

## Dataset
- Cleaned Google Play dataset: `googleplay_cleaned.csv`  
- Columns: `App`, `Reviews`, `Rating`  

> Note: Dashboard works with this cleaned dataset; no additional columns required.

---

## Installation & Setup

1. **Clone the repository**  
```bash
git clone https://github.com/<your-username>/futuristic-app-analytics.git
cd futuristic-app-analytics

2. Create virtual environment

python -m venv venv

3. Activate environment

Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

4.Install dependencies
pip install -r requirements.txt

5.Run the dashboard

streamlit run app.py

Future Improvements

Include Engagement Score (Reviews / Rating).
Add more interactive charts with hover tooltips or animated trends.
Support additional datasets (e.g., Categories, Installs) for deeper analytics.
