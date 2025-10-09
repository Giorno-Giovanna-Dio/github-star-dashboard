import os, json, requests, pandas as pd, plotly.express as px
from datetime import datetime

os.makedirs("assets", exist_ok=True)
os.makedirs("data", exist_ok=True)
HISTORY_PATH = "data/stars_history.json"

def fetch_top_repos():
    url = "https://api.github.com/search/repositories?q=stars:>10000&sort=stars&order=desc&per_page=30"
    data = requests.get(url).json()["items"]
    return {repo["full_name"]: repo["stargazers_count"] for repo in data}

def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    return {}

def save_history(snapshot):
    history = load_history()
    history[datetime.now().strftime("%Y-%m-%d")] = snapshot
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)

def compute_growth(current, previous):
    growth = {}
    for repo, stars in current.items():
        prev_stars = previous.get(repo, stars)
        growth[repo] = stars - prev_stars
    return growth

def render_chart(growth):
    df = pd.DataFrame([
        {"repo": k, "growth": v} for k, v in sorted(growth.items(), key=lambda x: x[1], reverse=True)[:15]
    ])
    fig = px.bar(
        df,
        x="growth", y="repo",
        orientation="h",
        title=f"Weekly Star Growth (Top 15)<br><sub>Updated {datetime.now().strftime('%Y-%m-%d')}</sub>",
        color="growth", color_continuous_scale="Sunset"
    )
    fig.update_layout(template="plotly_dark", height=600)
    fig.write_image("assets/stars_growth.svg")

if __name__ == "__main__":
    current = fetch_top_repos()
    history = load_history()
    if history:
        last_week = history[list(history.keys())[-1]]
        growth = compute_growth(current, last_week)
        render_chart(growth)
    save_history(current)
    print("✅ 星星成長率圖表完成")