import requests, pandas as pd, plotly.express as px, os
from datetime import datetime

os.makedirs("assets", exist_ok=True)

def fetch_open_issues():
    url = "https://api.github.com/search/repositories?q=stars:>10000&sort=stars&order=desc&per_page=50"
    data = requests.get(url).json()["items"]
    df = pd.DataFrame([
        {"repo": r["full_name"], "open_issues": r["open_issues_count"], "stars": r["stargazers_count"]}
        for r in data
    ])
    return df

def render_issues_chart(df):
    fig = px.box(
        df,
        y="open_issues",
        points="all",
        title=f"Distribution of Open Issues (Top 50 Repos)<br><sub>Updated {datetime.now().strftime('%Y-%m-%d')}</sub>",
        color_discrete_sequence=["#00E5FF"]
    )
    fig.update_layout(template="plotly_dark", yaxis_title="Open Issues")
    fig.write_image("assets/open_issues.svg")

if __name__ == "__main__":
    df = fetch_open_issues()
    render_issues_chart(df)
    print("✅ Open Issues 分布圖完成")