from fastapi import APIRouter, HTTPException
from backend.data import ModuleData
from backend.data.modules_data import load_all_modules

router = APIRouter(prefix="/api/modules", tags=["modules"])

# 启动时加载所有模块数据
load_all_modules()


@router.get("/chapters")
async def list_chapters():
    """获取所有章节（目录结构）"""
    return {"chapters": ModuleData.get_all_chapters()}


@router.get("/{module_id}")
async def get_module(module_id: str):
    """获取指定模块的完整内容"""
    module = ModuleData.get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail=f"模块 {module_id} 不存在")
    return {
        "id": module["id"],
        "title": module["title"],
        "description": module["description"],
        "prerequisites": module.get("prerequisites", []),
        "leads_to": module.get("leads_to", []),
        "tags": module.get("tags", []),
        "chapter": module["chapter"],
        "content_html": module["content_html"],
        "resources": module.get("resources", []),
    }


@router.get("/")
async def search_modules(q: str = ""):
    """搜索模块（关键词匹配标题、描述、标签）"""
    if not q:
        return {"modules": []}
    return {"modules": ModuleData.search(q)}
