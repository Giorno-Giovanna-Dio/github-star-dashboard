# scripts/update_readme.py
import re

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_section = "![GitHub Stars](./assets/stars_chart.svg)"
    updated = re.sub(
        r"<!--START_CHART-->.*<!--END_CHART-->",
        f"<!--START_CHART-->\n{new_section}\n<!--END_CHART-->",
        content,
        flags=re.S
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    update_readme()
    print("✅ README 已更新")