import requests, plotly.express as px, pandas as pd, os
from datetime import datetime
os.makedirs("assets", exist_ok=True)

def fetch_contributors_data():
    url = "https://api.github.com/search/repositories?q=stars:>5000&sort=stars&order=desc&per_page=50"
    repos = requests.get(url).json()["items"]

    result = []
    for r in repos:
        repo_name = r["full_name"]
        contributors_url = r["contributors_url"]
        contrib_data = requests.get(contributors_url).json()
        count = len(contrib_data) if isinstance(contrib_data, list) else 0
        result.append({"repo": repo_name, "contributors": count})

    return pd.DataFrame(result)

def render_contributors_chart(df):
    df = df.sort_values("contributors", ascending=False)[:20]
    fig = px.bar(
        df,
        x="contributors", y="repo",
        orientation="h",
        title=f"Contributor Count (Top 20 Repos)<br><sub>Updated {datetime.now().strftime('%Y-%m-%d')}</sub>",
        color="contributors",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(template="plotly_dark", height=600)
    fig.write_image("assets/contributors.svg")

if __name__ == "__main__":
    df = fetch_contributors_data()
    render_contributors_chart(df)