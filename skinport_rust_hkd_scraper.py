
import requests

# 汇率：1 EUR = 8.5 HKD（示例汇率）
exchange_rate = 8.5

# 目标关键词
target_keywords = ["Big Grin", "Glory AK47", "Tempered AK47"]

# 获取数据
url = "https://api.skinport.com/v1/items?app_id=730&currency=EUR"
headers = {"Accept": "application/json"}
response = requests.get(url, headers=headers)
items = response.json()

# 过滤并提取目标皮肤
html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Rust Skinport 港币价格</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: center; }
        img { height: 50px; }
    </style>
</head>
<body>
    <h2>Rust Skinport 港币价格</h2>
    <table>
        <thead><tr><th>皮肤名称</th><th>最低价格 (HKD)</th><th>图像</th></tr></thead>
        <tbody>
'''

for item in items:
    if isinstance(item, dict) and any(k.lower() in item.get("market_hash_name", "").lower() for k in target_keywords):
        name = item.get("market_hash_name", "")
        price_eur = item.get("min_price", 0)
        price_hkd = round(price_eur * exchange_rate, 2)
        img = item.get("image", "")
        html += f"<tr><td>{name}</td><td>HK${price_hkd}</td><td><img src='{img}' alt='{name}'></td></tr>"

html += '''
        </tbody>
    </table>
</body>
</html>
'''

# 写入 HTML 文件
with open("skinport_rust_hkd.html", "w", encoding="utf-8") as f:
    f.write(html)

print("已生成 skinport_rust_hkd.html")
