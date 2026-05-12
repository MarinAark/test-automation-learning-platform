"""
学习模块注册表 — 所有课程内容集中管理。
HTML 内容从 backend/data/modules/<id>.html 文件加载。
"""
from pathlib import Path

from backend.data import ModuleData

_MODULES_DIR = Path(__file__).parent / "modules"


def _html(module_id: str) -> str:
    """读取模块 HTML 文件内容"""
    return (_MODULES_DIR / f"{module_id}.html").read_text(encoding="utf-8")


def load_all_modules():
    """注册全部学习模块"""

    # ================================================================
    # 第一章：路线图与基础
    # ================================================================
    ModuleData.register("ch1", "路线图与基础", "📋", [
        {
            "id": "roadmap",
            "title": "学习路线图",
            "description": "从手工测试到 SDET 的 6 阶段路线图，预计 3-4 个月",
            "prerequisites": [],
            "leads_to": ["env-setup", "pytest-basics"],
            "tags": ["路线图", "职业规划"],
            "content_html": _html("roadmap"),
        },
        {
            "id": "skill-matrix",
            "title": "技能矩阵",
            "description": "入门→熟练→精通→专家 四级能力标准对照",
            "prerequisites": ["roadmap"],
            "leads_to": ["env-setup"],
            "tags": ["技能评估", "成长路径"],
            "content_html": _html("skill-matrix"),
        },
        {
            "id": "env-setup",
            "title": "环境搭建",
            "description": "Python 虚拟环境、依赖管理、项目骨架搭建",
            "prerequisites": [],
            "leads_to": ["api-client-encap", "pytest-basics"],
            "tags": ["环境", "pip", "venv"],
            "content_html": _html("env-setup"),
        },
        {
            "id": "pytest-basics",
            "title": "pytest 基础配置",
            "description": "pytest.ini 配置、markers、运行参数、断言机制",
            "prerequisites": ["env-setup"],
            "leads_to": ["pytest-fixtures", "api-client-encap"],
            "tags": ["pytest", "配置"],
            "content_html": _html("pytest-basics"),
        },
    ])

    # ================================================================
    # 第二章：接口自动化
    # ================================================================
    ModuleData.register("ch2", "接口自动化", "🔌", [
        {
            "id": "api-http-basics",
            "title": "HTTP 协议基础",
            "description": "RESTful 规范、HTTP 方法、状态码、请求/响应结构",
            "prerequisites": [],
            "leads_to": ["api-client-encap"],
            "tags": ["HTTP", "REST", "基础"],
            "content_html": _html("api-http-basics"),
        },
        {
            "id": "api-client-encap",
            "title": "requests 生产级封装",
            "description": "会话管理、重试策略、认证、日志、超时控制",
            "prerequisites": ["api-http-basics"],
            "leads_to": ["api-auth", "api-business-layer"],
            "tags": ["requests", "封装", "HTTP Client"],
            "content_html": _html("api-client-encap"),
        },
        {
            "id": "api-auth",
            "title": "认证与会话管理",
            "description": "Token 自动刷新、登录态维护、多种认证方式",
            "prerequisites": ["api-client-encap"],
            "leads_to": ["api-business-layer"],
            "tags": ["认证", "Token", "Session"],
            "content_html": _html("api-auth"),
        },
        {
            "id": "api-business-layer",
            "title": "业务层封装（三层架构）",
            "description": "Client→API→TestCase 分层设计，业务语义化方法",
            "prerequisites": ["api-client-encap", "api-auth"],
            "leads_to": ["api-schema", "api-data-driven", "api-e2e"],
            "tags": ["架构", "封装", "三层设计"],
            "content_html": _html("api-business-layer"),
        },
        {
            "id": "api-schema",
            "title": "JSON Schema 自动校验",
            "description": "基于 jsonschema 的响应结构校验，配合 OpenAPI 使用",
            "prerequisites": ["api-business-layer"],
            "leads_to": ["api-contract"],
            "tags": ["Schema", "校验", "jsonschema"],
            "content_html": _html("api-schema"),
        },
        {
            "id": "api-data-driven",
            "title": "数据驱动测试",
            "description": "JSON/YAML 测试数据与代码分离，参数化用例管理",
            "prerequisites": ["api-business-layer", "pytest-param"],
            "leads_to": ["api-e2e"],
            "tags": ["数据驱动", "JSON", "参数化"],
            "content_html": _html("api-data-driven"),
        },
        {
            "id": "api-contract",
            "title": "契约测试（Pact）",
            "description": "消费者驱动契约测试，微服务间 API 兼容性保证",
            "prerequisites": ["api-schema"],
            "leads_to": ["api-mock"],
            "tags": ["契约", "Pact", "微服务"],
            "content_html": _html("api-contract"),
        },
        {
            "id": "api-mock",
            "title": "Mock 服务隔离",
            "description": "responses 库、httpx MockTransport、WireMock",
            "prerequisites": ["api-client-encap"],
            "leads_to": ["api-e2e"],
            "tags": ["Mock", "隔离", "responses"],
            "content_html": _html("api-mock"),
        },
        {
            "id": "api-e2e",
            "title": "全链路场景测试",
            "description": "多服务串联的业务端到端流程测试",
            "prerequisites": ["api-business-layer", "api-auth", "api-schema"],
            "leads_to": ["ci-github"],
            "tags": ["E2E", "全链路", "场景"],
            "content_html": _html("api-e2e"),
        },
        {
            "id": "api-project",
            "title": "接口自动化项目结构",
            "description": "生产级接口测试框架的目录结构和配置",
            "prerequisites": ["api-business-layer"],
            "leads_to": ["ui-overview"],
            "tags": ["项目结构", "工程化"],
            "content_html": _html("api-project"),
        },
    ])

    # ================================================================
    # 第三章：UI 自动化
    # ================================================================
    ModuleData.register("ch3", "UI 自动化", "🖥️", [
        {
            "id": "ui-overview",
            "title": "工具选型对比",
            "description": "Playwright vs Selenium vs Cypress 对比分析",
            "prerequisites": ["api-project"],
            "leads_to": ["ui-playwright-core"],
            "tags": ["选型", "对比"],
            "content_html": _html("ui-overview"),
        },
        {
            "id": "ui-playwright-core",
            "title": "Playwright 核心用法",
            "description": "定位器、断言、自动等待、多浏览器、Trace",
            "prerequisites": ["ui-overview"],
            "leads_to": ["ui-pom", "ui-network"],
            "tags": ["Playwright", "核心"],
            "content_html": _html("ui-playwright-core"),
        },
        {
            "id": "ui-pom",
            "title": "Page Object 设计模式",
            "description": "元素定位集中管理，测试与页面解耦",
            "prerequisites": ["ui-playwright-core"],
            "leads_to": ["ui-components"],
            "tags": ["POM", "设计模式"],
            "content_html": _html("ui-pom"),
        },
        {
            "id": "ui-components",
            "title": "组件化封装",
            "description": "DataTable、Modal、DatePicker 等可复用组件",
            "prerequisites": ["ui-pom"],
            "leads_to": ["ui-project"],
            "tags": ["组件化", "复用"],
            "content_html": _html("ui-components"),
        },
        {
            "id": "ui-fixtures",
            "title": "Fixture 管理",
            "description": "Browser/Context/Page 生命周期、失败截图、命令行参数",
            "prerequisites": ["pytest-fixtures", "ui-playwright-core"],
            "leads_to": ["ui-visual"],
            "tags": ["fixture", "生命周期"],
            "content_html": _html("ui-fixtures"),
        },
        {
            "id": "ui-network",
            "title": "网络拦截 Mock",
            "description": "page.route() 拦截请求，模拟后端数据",
            "prerequisites": ["ui-playwright-core"],
            "leads_to": [],
            "tags": ["网络拦截", "Mock"],
            "content_html": _html("ui-network"),
        },
        {
            "id": "ui-visual",
            "title": "视觉回归测试",
            "description": "Playwright 内置截图对比，页面级视觉回归",
            "prerequisites": ["ui-fixtures"],
            "leads_to": [],
            "tags": ["视觉测试", "截图"],
            "content_html": _html("ui-visual"),
        },
        {
            "id": "ui-debug",
            "title": "Trace 调试",
            "description": "Playwright Trace Viewer 调试失败用例",
            "prerequisites": ["ui-playwright-core"],
            "leads_to": [],
            "tags": ["调试", "Trace"],
            "content_html": _html("ui-debug"),
        },
        {
            "id": "ui-project",
            "title": "UI 自动化项目结构",
            "description": "生产级 UI 测试框架目录结构",
            "prerequisites": ["ui-components"],
            "leads_to": ["ci-github"],
            "tags": ["项目结构"],
            "content_html": _html("ui-project"),
        },
    ])

    # ================================================================
    # 第四章：pytest 进阶
    # ================================================================
    ModuleData.register("ch4", "pytest 进阶", "⚙️", [
        {
            "id": "pytest-fixtures",
            "title": "Fixtures 深度用法",
            "description": "yield fixture、工厂模式、依赖链、scope 管理",
            "prerequisites": ["pytest-basics"],
            "leads_to": ["pytest-conftest", "pytest-param"],
            "tags": ["fixture", "进阶"],
            "content_html": _html("pytest-fixtures"),
        },
        {
            "id": "pytest-param",
            "title": "参数化高级用法",
            "description": "笛卡尔积、indirect、marks skip/xfail",
            "prerequisites": ["pytest-fixtures"],
            "leads_to": ["api-data-driven"],
            "tags": ["参数化", "parametrize"],
            "content_html": _html("pytest-param"),
        },
        {
            "id": "pytest-conftest",
            "title": "conftest 层级管理",
            "description": "多级 conftest 的覆盖规则和最佳实践",
            "prerequisites": ["pytest-fixtures"],
            "leads_to": [],
            "tags": ["conftest", "层级"],
            "content_html": _html("pytest-conftest"),
        },
        {
            "id": "pytest-plugins",
            "title": "插件生态",
            "description": "xdist、rerun、timeout、allure、bdd 等关键插件",
            "prerequisites": ["pytest-basics"],
            "leads_to": [],
            "tags": ["插件"],
            "content_html": _html("pytest-plugins"),
        },
        {
            "id": "pytest-hooks",
            "title": "Hook 机制",
            "description": "pytest 生命周期钩子，自定义行为",
            "prerequisites": ["pytest-fixtures"],
            "leads_to": [],
            "tags": ["Hook"],
            "content_html": _html("pytest-hooks"),
        },
    ])

    # ================================================================
    # 第五章：CI/CD
    # ================================================================
    ModuleData.register("ch5", "CI/CD 集成", "🚀", [
        {
            "id": "ci-github",
            "title": "GitHub Actions",
            "description": "CI Pipeline、矩阵测试、服务容器、制品上传",
            "prerequisites": ["api-project", "ui-project"],
            "leads_to": ["ci-docker"],
            "tags": ["CI", "GitHub Actions"],
            "content_html": _html("ci-github"),
        },
        {
            "id": "ci-jenkins",
            "title": "Jenkins Pipeline",
            "description": "声明式 Pipeline、参数化构建、通知",
            "prerequisites": ["ci-github"],
            "leads_to": [],
            "tags": ["Jenkins", "Pipeline"],
            "content_html": _html("ci-jenkins"),
        },
        {
            "id": "ci-docker",
            "title": "Docker + Selenium Grid",
            "description": "容器化测试执行、Selenium Grid 分布式",
            "prerequisites": ["ci-github"],
            "leads_to": [],
            "tags": ["Docker", "Grid"],
            "content_html": _html("ci-docker"),
        },
        {
            "id": "ci-allure",
            "title": "Allure 报告发布",
            "description": "GitHub Pages 自动发布测试报告",
            "prerequisites": ["ci-github"],
            "leads_to": [],
            "tags": ["Allure", "报告"],
            "content_html": _html("ci-allure"),
        },
    ])
