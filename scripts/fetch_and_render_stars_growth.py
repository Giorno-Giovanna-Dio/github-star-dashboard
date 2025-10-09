import os, json, requests, pandas as pd, plotly.express as px
from datetime import datetime

os.makedirs("assets", exist_ok=True)
os.makedirs("data", exist_ok=True)
HISTORY_PATH = "data/stars_history.json"

def fetch_top_repos():
    """從 GitHub API 抓取前 30 熱門專案"""
    url = "https://api.github.com/search/repositories?q=stars:>10000&sort=stars&order=desc&per_page=30"
    headers = {}
    # ✅ 加入 GitHub Token 避免 rate limit
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"⚠️ GitHub API failed: {res.status_code}")
        return {}
    data = res.json().get("items", [])
    return {repo["full_name"]: repo["stargazers_count"] for repo in data}

def load_history():
    """載入上週資料"""
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    return {}

def save_history(snapshot):
    """儲存本週 snapshot"""
    history = load_history()
    history[datetime.now().strftime("%Y-%m-%d")] = snapshot
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)

def compute_growth(current, previous):
    """比較本週 vs 上週星數變化"""
    growth = {}
    for repo, stars in current.items():
        prev_stars = previous.get(repo, stars)
        growth[repo] = stars - prev_stars
    return growth

def render_chart(growth):
    """生成長條圖（即使沒資料也安全）"""
    if not growth:
        fig = px.bar(x=[], y=[], title="No Data Available (GitHub API limit?)")
    else:
        df = pd.DataFrame([
            {"repo": k, "growth": v}
            for k, v in sorted(growth.items(), key=lambda x: x[1], reverse=True)[:15]
        ])
        fig = px.bar(
            df, x="growth", y="repo", orientation="h",
            title=f"Weekly Star Growth (Top 15)<br><sub>Updated {datetime.now().strftime('%Y-%m-%d')}</sub>",
            color="growth", color_continuous_scale="Sunset"
        )
    fig.update_layout(template="plotly_dark", height=600)
    fig.write_image("assets/stars_growth.svg")
    print("✅ 星星成長率圖表完成")

if __name__ == "__main__":
    current = fetch_top_repos()
    history = load_history()
    growth = {}
    if history:
        last_key = list(history.keys())[-1]
        last_week = history[last_key]
        growth = compute_growth(current, last_week)
    else:
        print("🆕 No previous data found — initializing history only.")
    render_chart(growth)
    save_history(current)