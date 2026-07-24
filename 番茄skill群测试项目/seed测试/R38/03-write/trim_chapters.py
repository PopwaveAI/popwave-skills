"""
R38 字数精简脚本
对ch002~ch005做字数精简到2000-2500字
只保留---前的正文，精简后重新附加交付面板
"""
import re
from pathlib import Path
import requests

DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"

OUTPUT_DIR = Path(r"d:\popwave-skills\番茄skill群测试项目\R38\03-write")

def count_chinese(text):
    """统计中文字数（去掉标点符号和markdown标记）"""
    # 移除markdown标题行
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        clean_lines.append(line)
    clean_text = ''.join(clean_lines)
    # 移除标点
    clean_text = re.sub(r'[，。！？；：、""''（）【】《》\s,.\!?;:\'\"\(\)\[\]<>—\-]', '', clean_text)
    return len(clean_text)

def trim_chapter(ch_file):
    """精简单章到2000-2500字"""
    content = ch_file.read_text(encoding="utf-8")
    
    # 分割正文和交付面板
    parts = content.split('---')
    main_text = parts[0]
    panel = '---' + '---'.join(parts[1:]) if len(parts) > 1 else ''
    
    current_count = count_chinese(main_text)
    if current_count <= 2500:
        print(f"{ch_file.name}: {current_count}字 ✅ 无需精简")
        return
    
    print(f"{ch_file.name}: {current_count}字 ❌ 开始精简...")
    
    # 调用API精简
    prompt = f"""请将以下网文正文精简到2000-2500字（中文字符数，不含标点）。

要求：
1. 保留核心事件、爽点、钩子不变
2. 删除冗余的环境描写、重复的感官描写、过度的心理活动
3. 保留系统面板格式【】
4. 保留动作链结构（2-3个细动作）
5. 保留多感官描写但每个场景只保留最强烈的1-2种感官
6. 保留章末钩子
7. 禁止改变剧情走向和人物行为
8. 精简后字数必须在2000-2500字之间

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
            {"role": "system", "content": "你是一位资深网文编辑，擅长精简正文同时保持节奏和爽感。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 3500,
        "temperature": 0.7,
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
        trimmed_text = result["choices"][0]["message"]["content"]
        
        # 验证精简后字数
        new_count = count_chinese(trimmed_text)
        if new_count > 2500:
            # 如果还是超，做硬截断（保留前2400字+钩子）
            print(f"  API精简后仍超：{new_count}字，做硬截断")
            lines = trimmed_text.split('\n')
            kept_lines = []
            char_count = 0
            for line in lines:
                line_clean = re.sub(r'[，。！？；：、""''（）【】《》\s,.\!?;:\'\"\(\)\[\]<>—\-]', '', line)
                char_count += len(line_clean)
                if char_count > 2400:
                    break
                kept_lines.append(line)
            trimmed_text = '\n'.join(kept_lines)
            new_count = count_chinese(trimmed_text)
        
        # 重新组合
        # 提取原标题
        title_match = re.match(r'^(# .+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else f"# {ch_file.stem}"
        
        # 精简后的正文（不带原标题，因为trimmed_text可能已含）
        if trimmed_text.startswith('#'):
            final_content = trimmed_text + '\n\n' + panel
        else:
            final_content = title + '\n\n' + trimmed_text + '\n\n' + panel
        
        ch_file.write_text(final_content, encoding="utf-8")
        print(f"  精简后：{new_count}字 {'✅' if 2000 <= new_count <= 2500 else '❌'}")
        
    except Exception as e:
        print(f"  精简失败: {e}")

# 执行
print("=" * 50)
print("R38 字数精简")
print("=" * 50)
for i in range(2, 6):
    ch_file = OUTPUT_DIR / f"ch00{i}.md"
    if ch_file.exists():
        trim_chapter(ch_file)
print("=" * 50)
