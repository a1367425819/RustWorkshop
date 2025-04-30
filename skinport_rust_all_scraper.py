import requests
from datetime import datetime

# Skinport Rust API（返回所有在售饰品）
url = "https://api.skinport.com/v1/items?app_id=252490&currency=USD"
headers = {"Accept-Encoding": "br"}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print("抓取失败：", e)
    exit()

# 过滤 + 按价格排序
filtered = []
for item in data:
    if not isinstance(item, dict):
        continue
    name = item.get("market_hash_name", "")
    price = item.get("min_price", 0)
    image = item.get("image", "")
    link = item.get("item_page", "")
    if name and price:
        filtered.append((name, float(price), image, link))

filtered.sort(key=lambda x: x[1])  # 按价格升序

# 生成 HTML
html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rust Skinport 全部饰品</title>
    <style>
        body { font-family: Arial; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        img { height: 50px; }
    </style>
</head>
<body>
    <h2>Rust Skinport 饰品价格一览</h2>
    <p>更新时间：''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
    <table>
        <thead><tr><th>名称</th><th>最低价格 (USD)</th><th>图片</th><th>链接</th></tr></thead>
        <tbody>
'''

for name, price, image, link in filtered:
    html += f"<tr><td>{name}</td><td>${price:.2f}</td><td><img src='{image}'></td><td><a href='{link}'>查看</a></td></tr>\n"

html += '''
        </tbody>
    </table>
</body>
</html>
'''

# 保存 HTML 文件
with open("rust_skinport_all.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ rust_skinport_all.html 已生成")