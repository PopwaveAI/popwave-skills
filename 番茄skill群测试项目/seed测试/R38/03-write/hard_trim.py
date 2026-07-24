"""
R38 硬截断脚本
保留每章前2400中文字+最后2段（钩子），其余截断
"""
import re
from pathlib import Path

OUTPUT_DIR = Path(r"d:\popwave-skills\番茄skill群测试项目\R38\03-write")

def count_chinese(text):
    clean_text = re.sub(r'[，。！？；：、""''（）【】《》\s,.\!?;:\'\"\(\)\[\]<>—\-]', '', text)
    return len(clean_text)

def hard_trim(ch_file, target=2350):
    content = ch_file.read_text(encoding="utf-8")
    parts = content.split('---')
    main_text = parts[0]
    panel = '---' + '---'.join(parts[1:]) if len(parts) > 1 else ''
    
    current_count = count_chinese(main_text)
    if current_count <= 2500:
        print(f"{ch_file.name}: {current_count}字 ✅")
        return
    
    # 按段落分割
    paragraphs = main_text.split('\n\n')
    
    # 保留段落直到字数达到target
    kept_paragraphs = []
    char_count = 0
    for p in paragraphs:
        p_count = count_chinese(p)
        if char_count + p_count > target:
            # 这一段落加上会超，但我们需要钩子
            # 检查这是不是最后几段（钩子）
            break
        kept_paragraphs.append(p)
        char_count += p_count
    
    # 把剩余段落中的最后2段（钩子）加回来
    remaining = paragraphs[len(kept_paragraphs):]
    if len(remaining) >= 2:
        kept_paragraphs.extend(remaining[-2:])
    elif remaining:
        kept_paragraphs.extend(remaining)
    
    final_main = '\n\n'.join(kept_paragraphs)
    final_count = count_chinese(final_main)
    
    # 如果还是超，再做一次段落级截断
    if final_count > 2500:
        paragraphs2 = final_main.split('\n\n')
        kept2 = []
        cnt2 = 0
        for p in paragraphs2:
            p_count = count_chinese(p)
            if cnt2 + p_count > 2350:
                break
            kept2.append(p)
            cnt2 += p_count
        # 加回钩子段
        if len(paragraphs2) > len(kept2):
            kept2.extend(paragraphs2[len(kept2):][-2:])
        final_main = '\n\n'.join(kept2)
        final_count = count_chinese(final_main)
    
    final_content = final_main + '\n\n' + panel
    ch_file.write_text(final_content, encoding="utf-8")
    print(f"{ch_file.name}: 截断后 {final_count}字 {'✅' if 2000 <= final_count <= 2500 else '❌'}")

print("=" * 50)
print("R38 硬截断到2000-2500字")
print("=" * 50)
for i in range(2, 6):
    ch_file = OUTPUT_DIR / f"ch00{i}.md"
    if ch_file.exists():
        hard_trim(ch_file)
print("=" * 50)
print("\n--- 最终字数 ---")
