#!/usr/bin/env python3
"""
[已废弃] pop-YouTubewebbuilder - inject.py

⚠️  此脚本已废弃（v3）。不再使用模板注入方式。
    请改用 v3 的设计原则 + agent 自主创作方式。
    保留此文件仅用于向后兼容，可能在任何未来版本中移除。
"""

import sys

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║  ⚠️  inject.py 已废弃 (v3)                               ║
║                                                          ║
║  v3 不再使用模板注入。请改用：                            ║
║                                                          ║
║    python scripts/run.py --channel-url <URL>              ║
║                                                          ║
║  然后让 agent 根据 SKILL.md 中的设计原则自主创作。        ║
║                                                          ║
║  保留此脚本仅用于向后兼容引用。                            ║
╚══════════════════════════════════════════════════════════╝
""")
    sys.exit(1)

if __name__ == "__main__":
    main()
