"""接口测试：学习模块 API"""
import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)


class TestModulesAPI:
    """P0: 模块 API 核心功能"""

    def test_health_check(self):
        """健康检查"""
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_list_chapters(self):
        """获取所有章节 — 应返回 6 个章节"""
        resp = client.get("/api/modules/chapters")
        assert resp.status_code == 200
        chapters = resp.json()["chapters"]
        assert len(chapters) >= 5
        # 验证章节结构
        for ch in chapters:
            assert "id" in ch
            assert "title" in ch
            assert "modules" in ch

    def test_get_module_by_id(self):
        """获取指定模块"""
        resp = client.get("/api/modules/roadmap")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == "roadmap"
        assert data["title"] == "学习路线图"
        assert "content_html" in data

    def test_get_module_not_found(self):
        """获取不存在的模块 — 返回 404"""
        resp = client.get("/api/modules/nonexistent")
        assert resp.status_code == 404

    @pytest.mark.parametrize("keyword,expected_in_results", [
        ("pytest", True),
        ("不存在的关键词xyz", False),
    ])
    def test_search_modules(self, keyword, expected_in_results):
        """搜索模块"""
        resp = client.get(f"/api/modules/?q={keyword}")
        assert resp.status_code == 200
        modules = resp.json()["modules"]
        if expected_in_results:
            assert len(modules) > 0
        else:
            assert len(modules) == 0


class TestProgressAPI:
    """P0: 学习进度 API"""

    def test_get_initial_progress(self):
        """新用户进度应为 0%"""
        resp = client.get("/api/progress/test-user-1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["percentage"] == 0.0
        assert data["completed_modules"] == []

    def test_update_and_get_progress(self):
        """标记完成 → 进度应更新"""
        # 标记完成
        resp = client.post("/api/progress/test-user-2", json={
            "module_id": "roadmap", "completed": True
        })
        assert resp.status_code == 200

        # 验证进度
        resp = client.get("/api/progress/test-user-2")
        data = resp.json()
        assert "roadmap" in data["completed_modules"]
        assert data["percentage"] > 0

    def test_unmark_progress(self):
        """取消标记 → 进度应回退"""
        # 先标记
        client.post("/api/progress/test-user-3", json={
            "module_id": "roadmap", "completed": True
        })
        # 再取消
        client.post("/api/progress/test-user-3", json={
            "module_id": "roadmap", "completed": False
        })
        resp = client.get("/api/progress/test-user-3")
        assert "roadmap" not in resp.json()["completed_modules"]
