import requests, plotly.express as px, os
from datetime import datetime

os.makedirs("assets", exist_ok=True)
topics = ["ai", "frontend", "backend", "game", "blockchain", "ml", "data"]

def fetch_topic_data():
    result = {}
    for topic in topics:
        url = f"https://api.github.com/search/repositories?q=topic:{topic}+stars:>1000"
        count = requests.get(url).json()["total_count"]
        result[topic] = count
    return result

def render_topics_chart(result):
    fig = px.bar(
        x=list(result.keys()), y=list(result.values()),
        title=f"Popular Topics (AI, Frontend, Game...)<br><sub>Updated {datetime.now().strftime('%Y-%m-%d')}</sub>",
        color=list(result.values()),
        color_continuous_scale="Magma"
    )
    fig.update_layout(template="plotly_dark", xaxis_title="Topic", yaxis_title="Repo Count")
    fig.write_image("assets/topic_keywords.svg")

if __name__ == "__main__":
    result = fetch_topic_data()
    render_topics_chart(result)