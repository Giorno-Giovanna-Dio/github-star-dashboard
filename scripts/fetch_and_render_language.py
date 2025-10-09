import requests, plotly.express as px, os
from datetime import datetime

os.makedirs("assets", exist_ok=True)

def fetch_language_data():
    url = "https://api.github.com/search/repositories?q=stars:>5000&sort=stars&order=desc&per_page=100"
    repos = requests.get(url).json()["items"]

    lang_count = {}
    for r in repos:
        lang = r["language"] or "Unknown"
        lang_count[lang] = lang_count.get(lang, 0) + 1

    return lang_count

def render_language_chart(lang_count):
    fig = px.pie(
        names=list(lang_count.keys()),
        values=list(lang_count.values()),
        title=f"Language Distribution (Top 100 Repos)<br><sub>Updated {datetime.now().strftime('%Y-%m-%d')}</sub>",
        color_discrete_sequence=px.colors.sequential.Aggrnyl
    )
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
    fig.write_image("assets/language_distribution.svg")

if __name__ == "__main__":
    data = fetch_language_data()
    render_language_chart(data)