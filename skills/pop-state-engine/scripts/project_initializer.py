#!/usr/bin/env python3
"""
项目初始化器 - 为 Popwave 项目创建引擎数据目录和 SQLite 数据库

改编自 OnKos 项目，删除 OnKos 特有目录结构（outline/drafts/revisions），
只创建 data/ 目录存放 novel_memory.db + project_config.json。
Popwave 的项目目录结构由 expert-writer step-0-init 创建，引擎不重复创建。
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class ProjectInitializer:
    """项目初始化器 - 创建引擎数据目录和数据库"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)

    def init_project(self, title: str = "", genre: str = "",
                     author: str = "", description: str = "") -> Dict[str, Any]:
        """
        初始化引擎数据目录

        Args:
            title: 小说标题
            genre: 题材类型
            author: 作者
            description: 简介

        Returns:
            初始化结果
        """
        result = {
            "project_path": str(self.project_path),
            "created_files": [],
            "created_dirs": [],
            "errors": []
        }

        try:
            self.project_path.mkdir(parents=True, exist_ok=True)

            # 只创建 data/ 目录（存放 novel_memory.db + project_config.json）
            data_dir = self.project_path / "data"
            data_dir.mkdir(exist_ok=True)
            result["created_dirs"].append(str(data_dir))

            # 精简的 project_config.json（删除 OnKos 的 auto_* 配置项）
            config = {
                "title": title or "未命名小说",
                "genre": genre or "玄幻",
                "author": author or "",
                "description": description or "",
                "created_at": datetime.now().isoformat(),
                "engine_version": "0.1.0",
            }

            config_path = data_dir / "project_config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            result["created_files"].append(str(config_path))

            # 初始化 SQLite 数据库（含全部 pop_ 前缀表）
            db_path = data_dir / "novel_memory.db"
            from memory_engine import MemoryEngine
            engine = MemoryEngine(str(db_path), project_path=str(self.project_path))
            engine.close()
            result["created_files"].append(str(db_path))

        except Exception as e:
            result["errors"].append(str(e))

        return result

    def get_project_status(self) -> Dict[str, Any]:
        """获取项目引擎状态"""
        status = {
            "project_path": str(self.project_path),
            "exists": self.project_path.exists(),
            "initialized": False,
            "stats": {}
        }

        if not self.project_path.exists():
            return status

        config_path = self.project_path / "data" / "project_config.json"
        if config_path.exists():
            status["initialized"] = True
            with open(config_path, 'r', encoding='utf-8') as f:
                status["config"] = json.load(f)

        db_path = self.project_path / "data" / "novel_memory.db"
        if db_path.exists():
            status["stats"]["database_size"] = db_path.stat().st_size
            status["stats"]["database_path"] = str(db_path)

        return status

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "init":
            return self.init_project(
                params.get("title", ""),
                params.get("genre", ""),
                params.get("author", ""),
                params.get("description", "")
            )
        elif action == "status":
            return self.get_project_status()
        else:
            raise ValueError(f"未知操作: {action}")

    def close(self):
        """无资源需释放，保留接口一致性"""
        pass


def main():
    parser = argparse.ArgumentParser(description='pop-state-engine 项目初始化器')
    parser.add_argument('--project-path', required=True, help='项目根目录')
    parser.add_argument('--action', required=True,
                       choices=['init', 'status'],
                       help='操作类型')
    parser.add_argument('--title', default='', help='小说标题')
    parser.add_argument('--genre', default='', help='题材类型')
    parser.add_argument('--author', default='', help='作者')
    parser.add_argument('--description', default='', help='简介')

    args = parser.parse_args()
    initializer = ProjectInitializer(args.project_path)

    skip_keys = {"project_path", "action", "output"}
    params = {k: v for k, v in vars(args).items()
              if k not in skip_keys and not k.startswith('_')}
    result = initializer.execute_action(args.action, params)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
