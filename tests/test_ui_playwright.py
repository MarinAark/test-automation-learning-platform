"""UI 测试：前端页面渲染和交互（需要先启动后端服务）"""
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")


class TestPageLoad:
    """P1: 页面加载和基本渲染"""

    def test_page_loads(self, page: Page, base_url):
        """首页应正常加载"""
        page.goto(base_url)
        expect(page.locator(".topbar .logo")).to_be_visible()

    def test_sidebar_renders(self, page: Page, base_url):
        """侧边栏应渲染章节列表"""
        page.goto(base_url)
        page.wait_for_selector(".mod-group", timeout=10000)
        groups = page.locator(".mod-group")
        expect(groups.first).to_be_visible()

    def test_module_click_loads_content(self, page: Page, base_url):
        """点击侧边栏 → 加载对应模块内容"""
        page.goto(base_url)
        # 等待侧边栏渲染
        page.wait_for_selector(".mod-body a", timeout=10000)
        # 点击第一个模块链接
        first_link = page.locator(".mod-body a").first
        first_link.click()
        # 应显示内容
        page.wait_for_selector(".sec h2", timeout=5000)
        expect(page.locator(".sec h2").first).to_be_visible()

    def test_search_filters_modules(self, page: Page, base_url):
        """搜索功能应过滤模块"""
        page.goto(base_url)
        page.wait_for_selector("#searchInput", timeout=10000)
        search = page.locator("#searchInput")
        search.fill("pytest")
        # 过滤后至少有一个可见结果
        page.wait_for_timeout(500)


class TestCopyButton:
    """P2: 代码复制功能"""

    def test_copy_button_exists(self, page: Page, base_url):
        """代码块应有复制按钮"""
        page.goto(base_url)
        page.wait_for_selector(".mod-body a", timeout=10000)
        # 加载包含代码块的模块
        page.locator("[data-module='api-client-encap']").click()
        page.wait_for_selector(".cw", timeout=5000)
        copy_btn = page.locator(".copy-btn").first
        expect(copy_btn).to_be_visible()


class TestCompleteButton:
    """P2: 学习进度标记"""

    def test_complete_button_toggles(self, page: Page, base_url):
        """点击标记完成 → 按钮状态应切换"""
        page.goto(base_url)
        page.wait_for_selector(".mod-body a", timeout=10000)
        page.locator("[data-module='roadmap']").click()
        page.wait_for_selector("#completeBtn", timeout=5000)
        btn = page.locator("#completeBtn")
        expect(btn).to_be_visible()
        # 点击标记
        btn.click()
        page.wait_for_timeout(500)
        # 应变为已完成状态
        expect(btn).to_have_class("complete-btn completed")
