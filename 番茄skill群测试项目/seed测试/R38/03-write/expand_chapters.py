"""
R38 字数补足脚本
精简后字数不足2000字，用API补写到2000-2500字
"""
import re
from pathlib import Path
import requests

DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"

OUTPUT_DIR = Path(r"d:\popwave-skills\番茄skill群测试项目\R38\03-write")

def count_chinese(text):
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        clean_lines.append(line)
    clean_text = ''.join(clean_lines)
    clean_text = re.sub(r'[，。！？；：、""''（）【】《》\s,.\!?;:\'\"\(\)\[\]<>—\-]', '', clean_text)
    return len(clean_text)

def expand_chapter(ch_file):
    content = ch_file.read_text(encoding="utf-8")
    parts = content.split('---')
    main_text = parts[0]
    panel = '---' + '---'.join(parts[1:]) if len(parts) > 1 else ''
    
    current_count = count_chinese(main_text)
    if 2000 <= current_count <= 2500:
        print(f"{ch_file.name}: {current_count}字 ✅")
        return
    
    if current_count >= 2000:
        return
    
    print(f"{ch_file.name}: {current_count}字 ❌ 需补写到2000-2500字")
    
    # 提取原标题
    title_match = re.match(r'^(# .+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else f"# {ch_file.stem}"
    
    prompt = f"""请将以下网文正文补写到2000-2500字（中文字符数，不含标点）。

要求：
1. 保留现有所有内容，不删减
2. 在适当位置补充内容，使总字数达到2200-2400字
3. 补充方向：
   - 增加动作链细节（把粗动作拆成2-3个细动作）
   - 增加感官描写（视觉/听觉/触觉/嗅觉，每场景2-3种感官）
   - 增加角色心理碎片（碎片化表达，不写完整分析句）
   - 增加环境氛围描写（1-2句即可）
4. 禁止改变剧情走向和人物行为
5. 禁止新增系统面板
6. 保留章末钩子
7. 补写后总字数必须在2000-2500字之间

当前字数：{current_count}字
目标字数：2200-2400字

原文：
{main_text}
"""
    headers = {
        "Authorization": f"Bearer {DS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": "你是一位资深番茄网文写手，擅长在保持节奏的前提下补充细节。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 3500,
        "temperature": 0.75,
        "stream": False
    }
    
    try:
        response = requests.post(
            f"{DS_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        result = response.json()
        expanded_text = result["choices"][0]["message"]["content"]
        
        new_count = count_chinese(expanded_text)
        print(f"  补写后：{new_count}字 {'✅' if 2000 <= new_count <= 2500 else '❌'}")
        
        if expanded_text.startswith('#'):
            final_content = expanded_text + '\n\n' + panel
        else:
            final_content = title + '\n\n' + expanded_text + '\n\n' + panel
        
        ch_file.write_text(final_content, encoding="utf-8")
        
    except Exception as e:
        print(f"  补写失败: {e}")

print("=" * 50)
print("R38 字数补足")
print("=" * 50)
for i in range(2, 6):
    ch_file = OUTPUT_DIR / f"ch00{i}.md"
    if ch_file.exists():
        expand_chapter(ch_file)
print("=" * 50)
