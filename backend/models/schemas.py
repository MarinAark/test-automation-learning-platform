from pydantic import BaseModel
from typing import Optional


class ModuleInfo(BaseModel):
    id: str
    title: str
    description: str
    prerequisites: list[str] = []
    leads_to: list[str] = []
    tags: list[str] = []
    content_html: str
    resources: list[dict] = []


class ModuleListItem(BaseModel):
    id: str
    title: str
    chapter: str
    tags: list[str] = []


class Chapter(BaseModel):
    id: str
    title: str
    icon: str
    modules: list[ModuleListItem]


class ProgressUpdate(BaseModel):
    module_id: str
    completed: bool


class ProgressResponse(BaseModel):
    completed_modules: list[str]
    total_modules: int
    percentage: float
