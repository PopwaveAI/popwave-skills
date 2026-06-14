#!/usr/bin/env python3
"""
批量检查网页URL状态
"""
import csv
import urllib.request
import urllib.error
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 创建SSL上下文，忽略证书验证
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def check_url(url, timeout=15):
    """检查单个URL的状态"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, context=ssl_context, timeout=timeout) as response:
            return url, response.status, "OK"
    except urllib.error.HTTPError as e:
        return url, e.code, f"HTTP Error: {e.reason}"
    except urllib.error.URLError as e:
        return url, None, f"URL Error: {e.reason}"
    except Exception as e:
        return url, None, f"Error: {str(e)}"

def extract_urls_from_csv(csv_path):
    """从CSV文件中提取URL"""
    urls = []
    # 尝试多种编码
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin1', 'cp1252']

    for encoding in encodings:
        try:
            with open(csv_path, 'r', encoding=encoding, errors='replace') as f:
                reader = csv.reader(f)
                header = next(reader, None)  # 跳过表头

                for row in reader:
                    if row and len(row) > 0:
                        url = row[0].strip()
                        # 清理URL（处理被引号包围或包含换行的情况）
                        url = url.replace('"', '').replace('\n', '').strip()
                        if url.startswith('http'):
                            urls.append(url)
            print(f"成功使用编码 {encoding} 读取文件，共提取 {len(urls)} 个URL")
            return urls
        except Exception as e:
            continue

    print("无法读取CSV文件")
    return []

def main():
    csv_path = '/Users/clairliu/Desktop/https___popwave.ai_-Performance-on-Search-2026-04-16/網頁.csv'

    print("正在提取URL...")
    urls = extract_urls_from_csv(csv_path)

    if not urls:
        print("未找到任何URL")
        return

    print(f"\n开始检查 {len(urls)} 个网页...")
    print("=" * 80)

    # 统计
    ok_count = 0
    error_count = 0
    error_urls = []

    # 使用线程池并行检查
    max_workers = 20  # 同时检查的数量

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls}

        for i, future in enumerate(as_completed(future_to_url), 1):
            url, status, message = future.result()

            if status == 200:
                ok_count += 1
                status_str = "✓ 正常"
            else:
                error_count += 1
                error_urls.append((url, status, message))
                status_str = f"✗ 异常 ({status or 'N/A'} - {message})"

            # 每检查10个显示一次进度
            if i % 10 == 0 or i == len(urls):
                print(f"[{i}/{len(urls)}] {status_str}: {url[:80]}...")

    # 输出结果
    print("\n" + "=" * 80)
    print("检查结果汇总")
    print("=" * 80)
    print(f"总计检查: {len(urls)} 个网页")
    print(f"正常访问: {ok_count} 个")
    print(f"访问异常: {error_count} 个")

    if error_urls:
        print("\n异常网页列表:")
        print("-" * 80)
        for url, status, message in error_urls:
            print(f"• {url}")
            print(f"  状态: {status or 'N/A'}, 错误: {message}")
            print()

        # 保存异常URL到文件
        error_file = '/Users/clairliu/陆虎个人网站/SEO/error_urls.txt'
        with open(error_file, 'w', encoding='utf-8') as f:
            for url, status, message in error_urls:
                f.write(f"{url}\t{status or 'N/A'}\t{message}\n")
        print(f"\n异常URL已保存到: {error_file}")

if __name__ == '__main__':
    main()
