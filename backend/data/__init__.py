from typing import Optional


class ModuleData:
    """学习模块数据库 — 生产环境可替换为 PostgreSQL/MongoDB"""

    _modules: dict = {}
    _chapters: list = []

    @classmethod
    def register(cls, chapter_id: str, chapter_title: str, icon: str,
                 modules: list[dict]):
        cls._chapters.append({
            "id": chapter_id,
            "title": chapter_title,
            "icon": icon,
            "modules": [{"id": m["id"], "title": m["title"],
                         "chapter": chapter_title, "tags": m.get("tags", [])}
                        for m in modules]
        })
        for m in modules:
            cls._modules[m["id"]] = {
                **m,
                "chapter": chapter_title,
                "chapter_id": chapter_id,
            }

    @classmethod
    def get_module(cls, module_id: str) -> Optional[dict]:
        return cls._modules.get(module_id)

    @classmethod
    def get_all_chapters(cls) -> list[dict]:
        return cls._chapters

    @classmethod
    def get_all_module_ids(cls) -> list[str]:
        return list(cls._modules.keys())

    @classmethod
    def search(cls, keyword: str) -> list[dict]:
        kw = keyword.lower()
        results = []
        for m in cls._modules.values():
            if (kw in m["title"].lower() or kw in m["description"].lower() or
                any(kw in t.lower() for t in m.get("tags", []))):
                results.append({
                    "id": m["id"], "title": m["title"],
                    "chapter": m["chapter"], "tags": m.get("tags", []),
                    "prerequisites": m.get("prerequisites", []),
                })
        return results
