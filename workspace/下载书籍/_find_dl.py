"""Find the download link for Wulin Banxia Zhuan TXT."""
import re
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
resp = requests.get("http://www.xqishuta.com/Shtml34905.html", headers=headers, timeout=15)
resp.encoding = "utf-8"
html = resp.text

# Search for download links
for m in re.finditer(r'href="([^"]+)"', html):
    href = m.group(1)
    if "txt" in href.lower():
        print(f"TXT in href: {href}")
    elif "34905" in href and href.endswith(".html") and "Shtml" not in href:
        print(f"34905 html link: {href}")
    elif "download" in href.lower() or "down" in href.lower():
        print(f"Download link: {href}")
