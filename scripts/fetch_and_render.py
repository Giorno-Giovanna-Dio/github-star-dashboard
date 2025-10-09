# scripts/fetch_and_render.py
import requests
import plotly.graph_objects as go
from datetime import datetime

def fetch_github_data():
    """從 GitHub API 抓取熱門專案資料"""
    url = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&per_page=100"
    res = requests.get(url)
    data = res.json()["items"]

    buckets = {"10k+": 0, "1k–10k": 0, "<1k": 0}
    for repo in data:
        stars = repo["stargazers_count"]
        if stars >= 10000:
            buckets["10k+"] += 1
        elif stars >= 1000:
            buckets["1k–10k"] += 1
        else:
            buckets["<1k"] += 1
    return buckets

def render_chart(buckets):
    """用 Plotly 畫出高質感圖表"""
    total = sum(buckets.values())
    labels = list(buckets.keys())
    values = list(buckets.values())
    colors = ["#FFD700", "#4CAF50", "#9E9E9E"]

    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo='label+percent',
            pull=[0.05, 0, 0],
        )]
    )

    fig.update_layout(
        template="plotly_dark",  # 黑底風格
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        title={
            "text": f"GitHub 星星分布（Top 100 Repos）<br><sub>更新時間：{datetime.now().strftime('%Y-%m-%d')}</sub>",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(size=18)
        },
        showlegend=False,
        margin=dict(l=20, r=20, t=80, b=20)
    )

    # 儲存成 SVG（可無損縮放）
    fig.write_image("assets/stars_chart.svg")

if __name__ == "__main__":
    buckets = fetch_github_data()
    render_chart(buckets)
    print("✅ 圖表生成完成：assets/stars_chart.svg")