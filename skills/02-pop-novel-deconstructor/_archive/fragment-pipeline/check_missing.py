import sqlite3

conn = sqlite3.connect("e:/AI小说/_shared/studio/scene_fragments.db")
done = {r[0] for r in conn.execute("SELECT DISTINCT chapter_number FROM scene_fragments WHERE source_book='深渊主宰'").fetchall()}
conn.close()

missing = sorted(set(range(1, 200)) - done)
print(f"1-200章中未处理: {len(missing)} 个")
print("前20个:", missing[:20])
