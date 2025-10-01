import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import altair as alt

# --- Page Config ---
st.set_page_config(page_title="Futuristic App Analytics", layout="wide")

# --- Fonts & Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
html, body, [class*="css"] {font-family: 'Roboto', sans-serif;}
</style>
""", unsafe_allow_html=True)

# --- Theme Toggle ---
theme = st.sidebar.radio("Select Theme", ["Light", "Dark"])
if theme == "Dark":
    bg_color = "#1E1E2F"
    card_bg = "#2C2C3D"
    font_color = "#ECF0F1"
    kpi_colors = {"high":"#2ECC71","medium":"#F1C40F","low":"#E74C3C"}
else:
    bg_color = "#F5F5F5"
    card_bg = "#FFFFFF"
    font_color = "#2C3E50"
    kpi_colors = {"high":"#2ECC71","medium":"#F1C40F","low":"#E74C3C"}

st.markdown(f"<body style='background-color:{bg_color}; color:{font_color}'>", unsafe_allow_html=True)
st.title("🚀 Futuristic App Analytics Dashboard")
st.markdown("---")

# --- Load Data ---
df = pd.read_csv("googleplay_cleaned.csv")

# --- Preprocessing ---
# Convert Reviews to numeric
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce').fillna(0)

# Sentiment
df['Sentiment'] = df['Rating'].apply(lambda x: "Positive" if x>=4 else "Neutral" if x==3 else "Negative")

# Performance Score
df['Performance Score'] = (df['Rating']*20 + df['Sentiment'].map({'Positive':80,'Neutral':50,'Negative':20})).clip(0,100).round(2)

# Hidden Gem Score
df['Hidden Gem Score'] = df['Rating'] * np.sqrt(df['Reviews'])

# --- Sidebar Filters ---
st.sidebar.header("⚙️ Filters")
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)
sentiment_options = st.sidebar.multiselect("Sentiment", ['Positive','Neutral','Negative'], default=['Positive','Neutral','Negative'])
top_n = st.sidebar.slider("Top N Apps", 1, 50, 10)

# Filtered dataframe
filtered_df = df[(df['Rating']>=min_rating) &
                 (df['Sentiment'].isin(sentiment_options))]
filtered_leaderboard = filtered_df.sort_values("Performance Score", ascending=False).head(top_n).reset_index(drop=True)

# --- KPI Card Function ---
def kpi_card(title, value, color="#2ECC71"):
    st.markdown(f"""
        <div style='background-color:{card_bg}; padding:20px; border-radius:15px; box-shadow:2px 2px 12px rgba(0,0,0,0.1); text-align:center; margin-bottom:10px;'>
            <h4 style='color:gray'>{title}</h4>
            <h2 style='color:{color}; margin:0'>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

# --- KPI Cards ---
st.subheader("📊 Key Metrics")
total_apps = len(filtered_df)
avg_rating = round(filtered_df['Rating'].mean(),2) if total_apps else 0
avg_positive = round((filtered_df['Sentiment']=="Positive").mean()*100,2) if total_apps else 0
top_score = filtered_leaderboard['Performance Score'].max() if total_apps else 0

k1,k2,k3,k4 = st.columns(4)
with k1: kpi_card("Total Apps", total_apps)
with k2: kpi_card("Avg Rating ⭐", avg_rating, color="#3498DB")
with k3: kpi_card("Positive Reviews %", f"{avg_positive}%", color="#2ECC71")
with k4: kpi_card("Top Score", top_score, color="#E67E22")

# --- Hidden Gems ---
st.subheader("💎 Hidden Gems")
hidden_gems = df.sort_values('Hidden Gem Score', ascending=False).head(5)
for i,row in hidden_gems.iterrows():
    st.markdown(f"**{i+1}. {row['App']}** | Rating: {row['Rating']} | Reviews: {row['Reviews']} | Score: {row['Hidden Gem Score']:.2f}")

# Engagement Score = Reviews divided by Rating
df['Engagement Score'] = (df['Reviews'] / df['Rating']).round(2)
st.subheader("🔥 Top Engaging Apps")
top_engagement = df.sort_values('Engagement Score', ascending=False).head(5)
for i, row in top_engagement.iterrows():
    st.markdown(f"**{i+1}. {row['App']}** | Rating: {row['Rating']} | Reviews: {row['Reviews']} | Engagement: {row['Engagement Score']}")
st.subheader("📈 Engagement Score Chart")
fig = px.bar(top_engagement, x='App', y='Engagement Score', text='Engagement Score',
             color='Engagement Score', color_continuous_scale='Viridis')
fig.update_layout(paper_bgcolor=bg_color, plot_bgcolor=bg_color, font_color=font_color, height=400)
st.plotly_chart(fig, use_container_width=True)


# --- Leaderboard with Sparklines ---
st.subheader("🏆 Leaderboard")
def highlight_score(val):
    if val >= 80: return f'background-color:{kpi_colors["high"]}; color:white'
    elif val >= 50: return f'background-color:{kpi_colors["medium"]}; color:white'
    else: return f'background-color:{kpi_colors["low"]}; color:white'

def sparkline(app_name):
    row = filtered_leaderboard[filtered_leaderboard['App']==app_name].iloc[0]
    trend = np.clip(np.random.normal(loc=row['Rating'], scale=0.2, size=5),1,5)
    days = pd.date_range(end=pd.Timestamp.today(), periods=5)
    df_trend = pd.DataFrame({'Day': days, 'Rating': trend})
    chart = alt.Chart(df_trend).mark_line(point=True).encode(x='Day', y='Rating').properties(width=100, height=40)
    return chart

for idx, row in filtered_leaderboard.iterrows():
    st.write(f"**{idx+1}. {row['App']}** - Score: {row['Performance Score']:.2f} | Sentiment: {row['Sentiment']}")
    st.altair_chart(sparkline(row['App']), use_container_width=False)

# --- Sentiment Pie Chart ---
st.subheader("📊 Sentiment Distribution")
sentiment_counts = filtered_df['Sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment','Count']
fig = px.pie(sentiment_counts, names='Sentiment', values='Count', color='Sentiment',
             color_discrete_map={'Positive':'#2ECC71','Neutral':'#F1C40F','Negative':'#E74C3C'})
fig.update_layout(paper_bgcolor=bg_color, font_color=font_color)
st.plotly_chart(fig, use_container_width=True)

# --- App Comparison ---
st.subheader("🔍 Compare Apps")
apps_to_compare = st.multiselect("Select up to 3 apps", filtered_leaderboard['App'].tolist(), default=filtered_leaderboard['App'].head(2).tolist())
if apps_to_compare:
    fig = go.Figure()
    for app_name in apps_to_compare:
        row = filtered_leaderboard[filtered_leaderboard['App']==app_name].iloc[0]
        trend = np.clip(np.random.normal(loc=row['Rating'], scale=0.2, size=5),1,5)
        days = pd.date_range(end=pd.Timestamp.today(), periods=5)
        fig.add_trace(go.Scatter(x=days, y=trend, mode='lines+markers', name=f"{app_name} ({row['Performance Score']} pts)"))
    fig.update_layout(title="App Rating Trend Comparison", height=350, plot_bgcolor=bg_color, paper_bgcolor=bg_color, font_color=font_color)
    st.plotly_chart(fig, use_container_width=True)

# --- Download Filtered Data ---
st.subheader("💾 Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download CSV", data=csv, file_name='filtered_apps.csv', mime='text/csv')

# --- Footer ---
st.markdown("---")
st.markdown(f"<div style='text-align:center; color:gray; padding:10px;'>Dashboard by <b>Viraj Kulye</b> | Futuristic App Analytics 🚀</div>", unsafe_allow_html=True)
