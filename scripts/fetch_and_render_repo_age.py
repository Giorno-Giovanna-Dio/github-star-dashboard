import requests, plotly.express as px, pandas as pd, os
from datetime import datetime

os.makedirs("assets", exist_ok=True)

def fetch_repo_age_data():
    url = "https://api.github.com/search/repositories?q=stars:>5000&sort=stars&order=desc&per_page=100"
    data = requests.get(url).json()["items"]
    df = pd.DataFrame([
        {"name": r["full_name"], "year": int(r["created_at"][:4])}
        for r in data
    ])
    return df

def render_repo_age_chart(df):
    fig = px.histogram(
        df,
        x="year",
        nbins=10,
        title=f"Repository Creation Year Distribution<br><sub>Updated {datetime.now().strftime('%Y-%m-%d')}</sub>",
        color_discrete_sequence=["#00E5FF"]
    )
    fig.update_layout(template="plotly_dark", xaxis_title="Year", yaxis_title="Repository Count")
    fig.write_image("assets/repo_age.svg")

if __name__ == "__main__":
    df = fetch_repo_age_data()
    render_repo_age_chart(df)