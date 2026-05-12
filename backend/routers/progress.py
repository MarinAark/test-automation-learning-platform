from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/progress", tags=["progress"])

# 简单的内存存储 — 生产环境替换为数据库
_progress_store: dict[str, set] = {}


class ProgressUpdate(BaseModel):
    module_id: str
    completed: bool


@router.get("/{user_id}")
async def get_progress(user_id: str):
    """获取用户学习进度"""
    total = __import__("backend.data", fromlist=["ModuleData"]).ModuleData.get_all_module_ids()
    completed = _progress_store.get(user_id, set())
    return {
        "user_id": user_id,
        "completed_modules": list(completed),
        "total_modules": len(total),
        "percentage": round(len(completed) / len(total) * 100, 1) if total else 0,
    }


@router.post("/{user_id}")
async def update_progress(user_id: str, body: ProgressUpdate):
    """更新学习进度"""
    if user_id not in _progress_store:
        _progress_store[user_id] = set()
    if body.completed:
        _progress_store[user_id].add(body.module_id)
    else:
        _progress_store[user_id].discard(body.module_id)
    return {"ok": True}
