import sqlite3

conn = sqlite3.connect("e:/AI小说/_shared/studio/scene_fragments.db")

total = conn.execute("SELECT COUNT(*) FROM scene_fragments WHERE source_book='深渊主宰'").fetchone()[0]
tagged = conn.execute("SELECT COUNT(*) FROM scene_fragments WHERE source_book='深渊主宰' AND scene_type IS NOT NULL").fetchone()[0]
chapters = conn.execute("SELECT COUNT(DISTINCT chapter_number) FROM scene_fragments WHERE source_book='深渊主宰'").fetchone()[0]
types = conn.execute("SELECT scene_type, COUNT(*) FROM scene_fragments WHERE source_book='深渊主宰' GROUP BY scene_type ORDER BY 2 DESC").fetchall()
sample = conn.execute("SELECT chapter_number, fragment_number, scene_type, substr(content,1,60) FROM scene_fragments WHERE source_book='深渊主宰' LIMIT 5").fetchall()

print(f"总片段: {total}   带标签: {tagged}   覆盖章节数: {chapters} / 1121")
print("scene_type 分布:")
for t in types:
    print(f"  {t[0]}: {t[1]}")
print("\n抽样片段:")
for r in sample:
    print(f"  ch{r[0]}-f{r[1]} [{r[2]}] {r[3]}")

conn.close()
