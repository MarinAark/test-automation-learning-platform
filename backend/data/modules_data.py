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
    # 第〇章：Python 基础
    # ================================================================
    ModuleData.register("ch0", "Python 基础", "🐍", [
        {
            "id": "python-intro",
            "title": "语言基础",
            "description": "变量、数据类型、控制流、列表推导式",
            "prerequisites": [],
            "leads_to": ["python-functions", "python-oop"],
            "tags": ["Python", "基础", "语法"],
            "content_html": _html("python-intro"),
            "resources": [
                {"title": "B站搜索：Python零基础入门", "url": "https://search.bilibili.com/all?keyword=Python零基础入门教程", "type": "video"},
                {"title": "Python官方教程（中文）", "url": "https://docs.python.org/zh-cn/3/tutorial/", "type": "article"},
            ],
        },
        {
            "id": "python-functions",
            "title": "函数与装饰器",
            "description": "函数定义、lambda、装饰器、生成器",
            "prerequisites": ["python-intro"],
            "leads_to": ["python-oop", "pytest-basics"],
            "tags": ["函数", "装饰器", "lambda"],
            "content_html": _html("python-functions"),
            "resources": [
                {"title": "B站搜索：Python装饰器详解", "url": "https://search.bilibili.com/all?keyword=Python装饰器详解", "type": "video"},
            ],
        },
        {
            "id": "python-oop",
            "title": "面向对象编程",
            "description": "类与对象、继承、多态、魔术方法",
            "prerequisites": ["python-functions"],
            "leads_to": ["python-modules", "api-client-encap"],
            "tags": ["OOP", "类", "继承"],
            "content_html": _html("python-oop"),
            "resources": [
                {"title": "B站搜索：Python面向对象编程", "url": "https://search.bilibili.com/all?keyword=Python面向对象编程OOP", "type": "video"},
            ],
        },
        {
            "id": "python-modules",
            "title": "模块与包管理",
            "description": "导入系统、包结构、虚拟环境详解",
            "prerequisites": ["python-oop"],
            "leads_to": ["env-setup"],
            "tags": ["模块", "包", "venv"],
            "content_html": _html("python-modules"),
        },
        {
            "id": "python-exceptions",
            "title": "异常处理与日志",
            "description": "try/except、自定义异常、logging 配置",
            "prerequisites": ["python-functions"],
            "leads_to": ["api-client-encap"],
            "tags": ["异常", "日志", "调试"],
            "content_html": _html("python-exceptions"),
        },
        {
            "id": "python-file-io",
            "title": "文件与数据处理",
            "description": "pathlib、JSON/CSV/YAML 读写",
            "prerequisites": ["python-intro"],
            "leads_to": ["api-data-driven"],
            "tags": ["文件", "JSON", "CSV"],
            "content_html": _html("python-file-io"),
            "resources": [
                {"title": "B站搜索：Python文件处理JSON", "url": "https://search.bilibili.com/all?keyword=Python+JSON数据驱动测试", "type": "video"},
            ],
        },
    ])

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
            "resources": [
                {"title": "B站搜索：测试开发学习路线", "url": "https://search.bilibili.com/all?keyword=测试开发学习路线", "type": "video"},
                {"title": "B站搜索：SDET技能树", "url": "https://search.bilibili.com/all?keyword=SDET自动化测试", "type": "video"},
            ],
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
            "resources": [
                {"title": "B站搜索：Python虚拟环境配置", "url": "https://search.bilibili.com/all?keyword=Python虚拟环境venv配置", "type": "video"},
                {"title": "Python官方文档：venv", "url": "https://docs.python.org/zh-cn/3/library/venv.html", "type": "article"},
            ],
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
            "resources": [
                {"title": "B站搜索：requests封装测试框架", "url": "https://search.bilibili.com/all?keyword=requests接口测试封装", "type": "video"},
                {"title": "requests官方文档", "url": "https://requests.readthedocs.io/", "type": "article"},
            ],
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
            "resources": [
                {"title": "B站搜索：Playwright自动化测试", "url": "https://search.bilibili.com/all?keyword=Playwright自动化测试教程", "type": "video"},
                {"title": "Playwright官方文档", "url": "https://playwright.dev/python/docs/intro", "type": "article"},
            ],
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
            "resources": [
                {"title": "B站搜索：pytest fixture高级用法", "url": "https://search.bilibili.com/all?keyword=pytest+fixture高级用法", "type": "video"},
                {"title": "pytest官方文档：fixtures", "url": "https://docs.pytest.org/en/stable/fixture.html", "type": "article"},
            ],
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
            "resources": [
                {"title": "B站搜索：GitHub Actions CI/CD", "url": "https://search.bilibili.com/all?keyword=GitHub+Actions+CI自动化测试", "type": "video"},
                {"title": "GitHub Actions文档", "url": "https://docs.github.com/actions", "type": "article"},
            ],
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

    # ================================================================
    # 第六章：工具平台
    # ================================================================
    ModuleData.register("ch6", "工具平台", "🛠️", [
        {
            "id": "report-center",
            "title": "测试报告中心",
            "description": "测试执行概况、趋势分析、失败原因分布、历史记录",
            "prerequisites": ["ci-allure"],
            "leads_to": [],
            "tags": ["报告", "Dashboard", "Chart.js"],
            "content_html": _html("report-center"),
        },
        {
            "id": "lowcode-editor",
            "title": "在线用例编辑器",
            "description": "可视化编排测试步骤，一键生成 Playwright Python 代码",
            "prerequisites": ["ui-playwright-core"],
            "leads_to": ["lowcode-pom"],
            "tags": ["低代码", "Playwright", "代码生成"],
            "content_html": _html("lowcode-editor"),
        },
        {
            "id": "lowcode-pom",
            "title": "POM 元素库管理",
            "description": "可视化管理 Page Object 页面与元素定位，支持导入导出",
            "prerequisites": ["ui-pom"],
            "leads_to": [],
            "tags": ["POM", "元素库", "localStorage"],
            "content_html": _html("lowcode-pom"),
        },
    ])
