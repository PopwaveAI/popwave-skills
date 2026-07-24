"""R38 字数统计脚本 - 仅统计---前的正文部分"""
import re
from pathlib import Path

OUTPUT_DIR = Path(r"d:\popwave-skills\番茄skill群测试项目\R38\03-write")
SEED_CH001 = Path(r"d:\popwave-skills\番茄skill群测试项目\R38\01-seed\ch001.md")

def count_main_text(file_path):
    """统计---前的正文字数（不含markdown标记和空行）"""
    content = file_path.read_text(encoding="utf-8")
    # 分割出正文部分
    parts = content.split('---')
    main_text = parts[0]
    # 移除markdown标题行(#开头)
    lines = main_text.split('\n')
    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        clean_lines.append(line)
    clean_text = ''.join(clean_lines)
    # 移除标点符号（中英文）
    clean_text = re.sub(r'[，。！？；：、""''（）【】《》\s,.\!?;:\'\"\(\)\[\]<>—\-]', '', clean_text)
    return len(clean_text)

print("=" * 50)
print("R38 字数统计（仅正文，不含交付面板）")
print("=" * 50)

# ch001 (seed产出)
count = count_main_text(SEED_CH001)
status = "✅" if 2000 <= count <= 2500 else "❌"
print(f"ch001 (seed): {count}字 {status}")

# ch002-ch005 (write产出)
for i in range(2, 6):
    ch_file = OUTPUT_DIR / f"ch00{i}.md"
    if ch_file.exists():
        count = count_main_text(ch_file)
        status = "✅" if 2000 <= count <= 2500 else "❌"
        print(f"ch00{i} (write): {count}字 {status}")
    else:
        print(f"ch00{i}: 文件不存在")

print("=" * 50)
