
import requests
from bs4 import BeautifulSoup
import time

# 配置需要查询的皮肤名称
skins = [
    "Tempered AK47",
    "Big Grin",
    "Glory AK47"
]

# 保存结果列表
results = []

# 遍历每个皮肤
for skin_name in skins:
    print(f"Searching Skinport for: {skin_name}")
    query = skin_name.replace(" ", "+")
    url = f"https://skinport.com/market?appId=252490&search={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        first_item = soup.select_one("a.sc-jrcTuL")

        if first_item:
            name = skin_name
            price = first_item.select_one("div.sc-dtBdUo").get_text(strip=True)
            img = first_item.select_one("img")["src"]
            results.append((name, price, img))
        else:
            results.append((skin_name, "N/A", "N/A"))
    except Exception as e:
        print(f"Error fetching {skin_name}: {e}")
        results.append((skin_name, "N/A", "N/A"))

    time.sleep(1)  # 避免请求过快

# 输出为 HTML 文件
html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rust Skins</title>
    <style>
        table { border-collapse: collapse; width: 100%%; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
        img { height: 50px; }
    </style>
</head>
<body>
    <h2>Rust Skinport 皮肤数据</h2>
    <table>
        <thead><tr><th>名称</th><th>价格 (EUR)</th><th>图片</th></tr></thead>
        <tbody>
"""

for name, price, img in results:
    html += f"<tr><td>{name}</td><td>{price}</td><td><img src='{img}' alt='{name}'></td></tr>\n"

html += """</tbody></table></body></html>"""

with open("rust_skin_data.html", "w", encoding="utf-8") as f:
    f.write(html)

print("数据已保存为 rust_skin_data.html")
