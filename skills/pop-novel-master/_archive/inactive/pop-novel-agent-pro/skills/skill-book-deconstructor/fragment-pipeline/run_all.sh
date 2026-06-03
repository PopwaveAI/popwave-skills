#!/bin/bash
set -e
cd "C:/Users/AWMPRO/.workbuddy/skills/skill-book-deconstructor/fragment-pipeline"

export DEEPSEEK_API_KEY="sk-da1d5162b41041f8a113112cec421f36"
export DEEPSEEK_BASE_URL="https://api.deepseek.com"
export DEEPSEEK_MODEL="deepseek-v4-flash"
export SCENE_FRAGMENTS_DB="e:/AI小说/_shared/studio/scene_fragments.db"

echo "=== 五书全量构建 ==="
echo "开始: $(date)"
echo "DB: $SCENE_FRAGMENTS_DB"

for book in "深渊主宰" "游戏之狩魔猎人" "战锤：以灰烬之名" "海贼法典" "玄鉴仙族"; do
    echo ""
    echo ">>> [$book] 开始 $(date)"
    python scripts/build_fragments.py --book "$book" --workers 8
    echo "<<< [$book] 完成 $(date)"
done

echo ""
echo "=== 全部完成 $(date) ==="

# 统计
python -c "
import sqlite3
conn = sqlite3.connect('$SCENE_FRAGMENTS_DB')
c = conn.cursor()
for book in ['深渊主宰','游戏之狩魔猎人','战锤：以灰烬之名','海贼法典','玄鉴仙族']:
    c.execute('SELECT COUNT(*), COUNT(DISTINCT chapter_number), SUM(word_count) FROM scene_fragments WHERE source_book=?', (book,))
    f, ch, wc = c.fetchone()
    print(f'{book}: {f}片段, {ch}章, {wc}字')
conn.close()
"