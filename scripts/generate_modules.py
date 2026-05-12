#!/usr/bin/env python3
"""Generate HTML snippet files for each learning module."""
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "backend", "data", "modules")
os.makedirs(BASE, exist_ok=True)

def write_html(filename, content):
    with open(os.path.join(BASE, filename), "w", encoding="utf-8") as f:
        f.write(content)

# ===== Ch1 =====
write_html("roadmap.html", """<h3>学习路线图</h3>
<div class="rm">
<div class="ms"><div class="mt">阶段一：Python 测试基础（2周）</div><div class="md">pytest 高级用法、fixture、参数化、conftest</div><div class="tags"><span>pytest</span><span>fixtures</span></div></div>
<div class="ms"><div class="mt">阶段二：接口自动化核心（4周）</div><div class="md">requests/httpx 封装、Schema校验、Mock、契约测试</div><div class="tags"><span>requests</span><span>httpx</span></div></div>
<div class="ms"><div class="mt">阶段三：UI 自动化核心（4周）</div><div class="md">Playwright、POM、组件化、视觉回归、Trace</div><div class="tags"><span>Playwright</span><span>POM</span></div></div>
<div class="ms"><div class="mt">阶段四：框架整合（2周）</div><div class="md">多环境配置、Allure报告、并发执行</div><div class="tags"><span>Allure</span><span>parallel</span></div></div>
<div class="ms"><div class="mt">阶段五：CI/CD 集成（2周）</div><div class="md">GitHub Actions、Jenkins、Docker</div><div class="tags"><span>CI/CD</span><span>Docker</span></div></div>
<div class="ms"><div class="mt">阶段六：性能与安全（2周）</div><div class="md">locust、OWASP ZAP</div><div class="tags"><span>locust</span><span>security</span></div></div>
</div>""")

write_html("skill-matrix.html", """<h3>技能矩阵</h3>
<table>
<tr><th>技能域</th><th>入门</th><th>熟练</th><th>精通</th><th>专家</th></tr>
<tr><td>接口自动化</td><td>会用requests</td><td>封装客户端、认证</td><td>Schema校验、Mock</td><td>契约测试、全链路</td></tr>
<tr><td>UI自动化</td><td>录制回放</td><td>POM分层</td><td>组件化、视觉回归</td><td>多平台统一框架</td></tr>
<tr><td>pytest</td><td>写test_函数</td><td>fixture分层</td><td>插件开发</td><td>定制测试框架</td></tr>
<tr><td>CI/CD</td><td>本地运行</td><td>Actions单步</td><td>Pipeline、Docker</td><td>多环境自动部署</td></tr>
</table>""")

write_html("env-setup.html", """<h3>环境搭建</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">Terminal</span></div>
<pre><code>mkdir test-automation-framework && cd test-automation-framework
python3 -m venv venv
source venv/bin/activate

pip install pytest pytest-xdist pytest-rerunfailures pytest-timeout
pip install requests httpx jsonschema pydantic
pip install playwright allure-pytest
playwright install --with-deps chromium

pip freeze > requirements.txt</code></pre></div>""")

write_html("pytest-basics.html", """<h3>pytest.ini 配置</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">pytest.ini</span></div>
<pre><code>[pytest]
minversion = 7.0
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --maxfail=5
    -n auto
    --reruns 2
    --alluredir=allure-results
markers =
    smoke: 冒烟测试
    regression: 回归测试
    p0: 核心功能
    p1: 重要功能
    p2: 边缘场景</code></pre></div>""")

# ===== Ch2: API =====
write_html("api-http-basics.html", """<h3>HTTP 方法与状态码</h3>
<table>
<tr><th>方法</th><th>语义</th><th>幂等</th><th>安全</th><th>典型状态码</th></tr>
<tr><td>GET</td><td>获取资源</td><td>Yes</td><td>Yes</td><td>200 / 404</td></tr>
<tr><td>POST</td><td>创建资源</td><td>No</td><td>No</td><td>201 / 422</td></tr>
<tr><td>PUT</td><td>全量更新</td><td>Yes</td><td>No</td><td>200 / 204</td></tr>
<tr><td>PATCH</td><td>部分更新</td><td>No</td><td>No</td><td>200</td></tr>
<tr><td>DELETE</td><td>删除资源</td><td>Yes</td><td>No</td><td>204 / 404</td></tr>
</table>""")

write_html("api-client-encap.html", """<h3>生产级 HTTP 客户端封装</h3>
<p style="color:var(--text2);margin-bottom:12px;">封装<strong>会话管理、认证、重试、日志、超时</strong>等能力。</p>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">core/api_client.py</span></div>
<pre><code>import json, logging
from typing import Optional
from dataclasses import dataclass, field
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


@dataclass
class APIConfig:
    base_url: str
    token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    timeout: int = 30
    retry_count: int = 3
    verify_ssl: bool = True
    extra_headers: dict = field(default_factory=dict)


class APIClient:

    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            **config.extra_headers,
        })

        # Token auth
        if config.token:
            self.session.headers["Authorization"] = f"Bearer {config.token}"
        elif config.username and config.password:
            self.session.auth = (config.username, config.password)

        # Retry: only on 5xx/429
        retry = Retry(
            total=config.retry_count, backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _request(self, method, path, **kwargs):
        url = urljoin(self.config.base_url, path)
        timeout = kwargs.pop("timeout", self.config.timeout)
        logger.info(f"-> {method} {url}")
        resp = self.session.request(method, url, timeout=timeout,
                                     verify=self.config.verify_ssl, **kwargs)
        logger.info(f"<- {resp.status_code} [{len(resp.content)}b]")
        return resp

    def get(self, p, params=None, **kw):
        return self._request("GET", p, params=params, **kw)
    def post(self, p, data=None, **kw):
        return self._request("POST", p, json=data, **kw)
    def put(self, p, data=None, **kw):
        return self._request("PUT", p, json=data, **kw)
    def delete(self, p, **kw):
        return self._request("DELETE", p, **kw)
    def close(self):
        self.session.close()</code></pre></div>""")

write_html("api-auth.html", """<h3>Token 自动刷新管理器</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">core/auth_manager.py</span></div>
<pre><code>import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenInfo:
    access_token: str
    refresh_token: str
    expires_at: float  # unix timestamp

    def is_expired(self) -> bool:
        return time.time() >= self.expires_at - 60  # refresh early


class AuthManager:
    '''Auto-login + auto-refresh + expired re-login'''

    def __init__(self, client):
        self.client = client
        self.token_info: Optional[TokenInfo] = None

    def login(self, username, password) -> TokenInfo:
        resp = self.client.post("/auth/login", data={
            "username": username, "password": password
        })
        assert resp.status_code == 200, f"Login failed: {resp.text}"
        data = resp.json()
        self.token_info = TokenInfo(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_at=time.time() + data.get("expires_in", 3600),
        )
        self.client.session.headers["Authorization"] = \
            f"Bearer {self.token_info.access_token}"
        return self.token_info

    def ensure_valid_token(self):
        if not self.token_info:
            raise RuntimeError("Call login() first")
        if self.token_info.is_expired():
            resp = self.client.post("/auth/refresh", data={
                "refresh_token": self.token_info.refresh_token
            })
            if resp.status_code == 200:
                data = resp.json()
                self.token_info.access_token = data["access_token"]
                self.token_info.expires_at = time.time() + data["expires_in"]
                self.client.session.headers["Authorization"] = \
                    f"Bearer {data['access_token']}"
            else:
                raise RuntimeError("Token refresh failed, re-login needed")</code></pre></div>""")

write_html("api-business-layer.html", """<h3>三层架构：Client -> API Wrapper -> TestCase</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">apis/user_api.py</span></div>
<pre><code>class UserAPI:
    '''Business-layer: semantic methods wrapping HTTP details'''

    def __init__(self, client):
        self.c = client
        self.prefix = "/api/v1/users"

    def create(self, name, email, role="user"):
        resp = self.c.post(self.prefix, data={
            "name": name, "email": email, "role": role
        })
        assert resp.status_code == 201, f"Create failed: {resp.text}"
        return resp.json()

    def get(self, uid):
        resp = self.c.get(f"{self.prefix}/{uid}")
        assert resp.status_code == 200
        return resp.json()

    def search(self, keyword=None, role=None, page=1, size=20):
        params = {"page": page, "size": size}
        if keyword: params["q"] = keyword
        if role: params["role"] = role
        return self.c.get(self.prefix, params=params).json()

    def update(self, uid, **fields):
        resp = self.c.put(f"{self.prefix}/{uid}", data=fields)
        assert resp.status_code == 200
        return resp.json()

    def delete(self, uid):
        assert self.c.delete(f"{self.prefix}/{uid}").status_code == 204


# ===== Test layer =====
class TestUserCRUD:

    def test_create_and_get(self, api):
        created = api.create(name="Alice", email="a@test.com", role="admin")
        fetched = api.get(created["id"])
        assert fetched["name"] == "Alice"
        assert fetched["role"] == "admin"
        api.delete(created["id"])</code></pre></div>""")

write_html("api-schema.html", """<h3>JSON Schema 自动校验</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">core/schema_validator.py</span></div>
<pre><code>import json
from pathlib import Path
from jsonschema import validate, ValidationError


class SchemaValidator:

    def __init__(self, schemas_dir="schemas"):
        self.schemas = {}
        for f in Path(schemas_dir).glob("*.json"):
            self.schemas[f.stem] = json.loads(f.read_text())

    def validate(self, schema_name, data):
        try:
            validate(instance=data, schema=self.schemas[schema_name])
        except ValidationError as e:
            raise AssertionError(f"Schema failed: {e.message}")


# schemas/user.json
'''
{
  "type": "object",
  "required": ["id", "name", "email", "role"],
  "properties": {
    "id":    {"type": "integer", "minimum": 1},
    "name":  {"type": "string", "minLength": 1, "maxLength": 100},
    "email": {"type": "string", "format": "email"},
    "role":  {"type": "string", "enum": ["user", "admin"]}
  },
  "additionalProperties": false
}
'''

# Usage
def test_schema(api, validator):
    user = api.create(name="test", email="t@t.com")
    validator.validate("user", user)  # auto-validate structure</code></pre></div>""")

write_html("api-data-driven.html", """<h3>数据驱动测试</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">tests/test_data_driven.py</span></div>
<pre><code>import json, pytest
from pathlib import Path


def load_cases(filename):
    path = Path(__file__).parent / "testdata" / filename
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", load_cases("user_cases.json"),
                         ids=lambda c: c["name"])
def test_create_user(api, case):
    resp = api.c.post("/api/v1/users", data=case["payload"])
    assert resp.status_code == case["expected_status"]
    if case.get("expected_field"):
        assert case["expected_field"] in resp.json().get("errors", {})
    if resp.status_code == 201:
        api.delete(resp.json()["id"])


# testdata/user_cases.json
'''
[
  {"name":"Normal", "payload":{"name":"A","email":"a@b.com"}, "expected_status":201},
  {"name":"Missing name", "payload":{"email":"a@b.com"}, "expected_status":422},
  {"name":"Bad email", "payload":{"name":"A","email":"bad"}, "expected_status":422}
]
'''</code></pre></div>""")

write_html("api-contract.html", """<h3>契约测试 (Pact)</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">tests/contract/test_user_contract.py</span></div>
<pre><code>import pytest
from pact import Consumer, Provider


@pytest.fixture(scope="session")
def pact():
    pact = Consumer("UserWeb").has_pact_with(
        Provider("UserService"), port=1234
    )
    pact.start_service()
    yield pact
    pact.stop_service()


def test_user_contract(pact):
    expected = {"id": 1, "name": "Alice", "email": "a@test.com"}

    pact.given("User id=1 exists") \
        .upon_receiving("GET user detail") \
        .with_request(method="GET", path="/api/v1/users/1") \
        .will_respond_with(status=200, body=expected)

    with pact:
        assert UserAPI(client).get(1) == expected</code></pre></div>""")

write_html("api-mock.html", """<h3>Mock 服务隔离</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">tests/test_with_mock.py</span></div>
<pre><code>import responses


@responses.activate
def test_order_when_payment_down(api):
    '''Verify order service degrades when payment is unavailable'''
    responses.add(responses.POST, "https://payment.internal/pay",
                  json={"error": "Service Unavailable"}, status=503)

    resp = api.c.post("/api/v1/orders", data={"product_id": 1})
    assert resp.status_code == 202
    assert resp.json()["status"] == "pending_payment"</code></pre></div>""")

write_html("api-e2e.html", """<h3>全链路场景测试</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">tests/test_e2e_order_flow.py</span></div>
<pre><code>class TestOrderE2E:
    '''Register -> Login -> Order -> Pay -> Verify'''

    def test_full_flow(self, client, user_api, order_api, payment_api):
        # 1. Register
        user = user_api.create(name="E2E User", email="e2e@test.com")
        # 2. Login
        auth = AuthManager(client)
        auth.login(user["name"], "Test@123")
        # 3. Create order
        order = order_api.create(product_id=100, quantity=2)
        assert order["status"] == "pending_payment"
        # 4. Pay
        payment = payment_api.pay(order["id"], method="wechat")
        assert payment["status"] == "success"
        # 5. Verify status updated
        updated = order_api.get(order["id"])
        assert updated["status"] == "paid"
        # Cleanup
        order_api.cancel(order["id"])
        user_api.delete(user["id"])</code></pre></div>""")

write_html("api-project.html", """<h3>接口自动化项目结构</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">api_test_framework/</span></div>
<pre><code>api_test_framework/
├── config/settings.yaml         # Multi-env config
├── core/
│   ├── api_client.py            # HTTP Client (retry/auth/logging)
│   ├── auth_manager.py          # Token manager
│   └── schema_validator.py      # JSON Schema validator
├── apis/                        # Business wrappers
│   ├── user_api.py
│   ├── order_api.py
│   └── payment_api.py
├── schemas/                     # JSON Schema files
├── testdata/                    # Data-driven cases
├── tests/
│   ├── conftest.py
│   ├── test_user_crud.py
│   ├── test_user_data_driven.py
│   └── contract/
├── utils/
│   ├── logger.py
│   └── faker_helper.py
├── pytest.ini
└── requirements.txt</code></pre></div>""")

# ===== Ch3: UI =====
write_html("ui-overview.html", """<h3>UI 自动化工具对比</h3>
<table>
<tr><th>工具</th><th>语言</th><th>优势</th><th>适用场景</th></tr>
<tr><td><strong>Playwright</strong> <span class="badge b-green">推荐</span></td><td>多语言</td><td>auto-wait、Trace、网络拦截、多浏览器</td><td>现代Web、SPA</td></tr>
<tr><td>Selenium 4</td><td>全语言</td><td>生态成熟、Grid分布式</td><td>遗留系统</td></tr>
<tr><td>Cypress</td><td>JS/TS</td><td>开发体验好</td><td>前端团队主导</td></tr>
</table>""")

write_html("ui-playwright-core.html", """<h3>Playwright 测试用例</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">tests/ui/test_login.py</span></div>
<pre><code>import pytest
from playwright.sync_api import Page, expect


class TestLogin:

    @pytest.fixture(autouse=True)
    def goto_login(self, page: Page):
        page.goto("/login")
        page.wait_for_load_state("networkidle")

    def test_login_success(self, page: Page):
        '''P0: Normal login flow'''
        page.get_by_label("Username").fill("admin")
        page.get_by_label("Password").fill("Test@123456")
        page.get_by_role("button", name="Login").click()

        # Playwright auto-waits for element visibility
        expect(page.get_by_text("Welcome back")).to_be_visible()
        expect(page).to_have_url("/dashboard")

        # Verify localStorage token
        token = page.evaluate("() => localStorage.getItem('access_token')")
        assert token is not None

    @pytest.mark.parametrize("user,pwd,err", [
        ("admin", "wrong", "Invalid credentials"),
        ("", "Test@123", "Username required"),
    ])
    def test_login_validation(self, page, user, pwd, err):
        page.get_by_label("Username").fill(user)
        page.get_by_label("Password").fill(pwd)
        page.get_by_role("button", name="Login").click()
        expect(page.get_by_text(err)).to_be_visible()</code></pre></div>""")

write_html("ui-pom.html", """<h3>Page Object 设计模式</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">pages/login_page.py</span></div>
<pre><code>class LoginPage:
    '''Elements centralized - change once, fix everywhere'''

    def __init__(self, page):
        self.p = page
        self.url = "/login"
        self.username = page.get_by_label("Username")
        self.password = page.get_by_label("Password")
        self.submit = page.get_by_role("button", name="Login")

    def goto(self):
        self.p.goto(self.url)
        return self

    def login(self, user, pwd):
        self.username.fill(user)
        self.password.fill(pwd)
        self.submit.click()
        return DashboardPage(self.p)


class DashboardPage:
    def __init__(self, page):
        self.p = page

    def assert_loaded(self):
        expect(self.p).to_have_url("/dashboard")
        return self


# Test becomes extremely clean
def test_login(page):
    LoginPage(page).goto().login("admin", "Test@123").assert_loaded()</code></pre></div>""")

write_html("ui-components.html", """<h3>组件化封装</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">components/data_table.py</span></div>
<pre><code>class DataTable:
    '''Reusable table component for any Page'''

    def __init__(self, page, selector):
        self.container = page.locator(selector)
        self.rows = self.container.locator("tbody tr")

    def count(self): return self.rows.count()
    def assert_has_row(self, text):
        expect(self.rows.filter(has_text=text)).to_have_count(1)
    def click_row(self, text):
        self.rows.filter(has_text=text).click()


class Modal:
    def __init__(self, page):
        self.dlg = page.locator(".modal")
    def confirm(self): self.dlg.get_by_text("OK").click()
    def cancel(self): self.dlg.get_by_text("Cancel").click()</code></pre></div>""")

write_html("ui-fixtures.html", """<h3>浏览器 Fixture 管理</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">tests/ui/conftest.py</span></div>
<pre><code>import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path


@pytest.fixture(scope="session")
def browser(request):
    '''Session-level: launch browser once for all tests'''
    browser_type = request.config.getoption("--browser", default="chromium")
    headed = request.config.getoption("--headed", default=False)
    with sync_playwright() as p:
        b = getattr(p, browser_type).launch(headless=not headed)
        yield b
        b.close()


@pytest.fixture
def page(browser, request):
    '''Per-test Page + auto-screenshot on failure'''
    ctx = browser.new_context(viewport={"width":1920,"height":1080})
    page = ctx.new_page()
    yield page
    # Auto screenshot on failure
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        Path("screenshots").mkdir(exist_ok=True)
        page.screenshot(path=f"screenshots/{request.node.name}.png")
    ctx.close()</code></pre></div>""")

write_html("ui-network.html", """<h3>网络拦截 Mock</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">tests/ui/test_network_mock.py</span></div>
<pre><code>def test_empty_dashboard(page):
    '''Mock API returning empty data -> verify empty state UI'''
    page.route("**/api/v1/orders?**", lambda r: r.fulfill(
        status=200, content_type="application/json",
        body='{"items":[], "total":0}',
    ))
    page.goto("/dashboard")
    expect(page.get_by_text("No data yet")).to_be_visible()


def test_server_error(page):
    '''Mock 500 error -> verify error handling UI'''
    page.route("**/api/**", lambda r: r.fulfill(status=500))
    page.goto("/dashboard")
    expect(page.get_by_text("Something went wrong")).to_be_visible()</code></pre></div>""")

write_html("ui-visual.html", """<h3>视觉回归测试</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">tests/ui/test_visual.py</span></div>
<pre><code>def test_dashboard_snapshot(page, assert_snapshot):
    page.goto("/dashboard")
    page.wait_for_load_state("networkidle")
    assert_snapshot(page.screenshot(full_page=True))


def test_button_states(page):
    page.goto("/form")
    btn = page.get_by_role("button", name="Submit")
    for state in ["default", "hover", "focus", "disabled"]:
        if state == "hover": btn.hover()
        elif state == "focus": btn.focus()
        expect(btn.screenshot()).to_match_snapshot(f"btn_{state}.png")</code></pre></div>""")

write_html("ui-debug.html", """<h3>Trace 调试</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">启用 Trace</span></div>
<pre><code># CLI
pytest --tracing=retain-on-failure   # Only on failure
pytest --tracing=on                   # All tests

# Code
context.tracing.start(screenshots=True, snapshots=True)
# ... test ...
context.tracing.stop(path="trace.zip")
# View: playwright show-trace trace.zip</code></pre></div>""")

write_html("ui-project.html", """<h3>UI 自动化项目结构</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">ui_test_framework/</span></div>
<pre><code>ui_test_framework/
├── pages/                    # Page Objects
│   ├── login_page.py
│   └── dashboard_page.py
├── components/               # Reusable components
│   ├── data_table.py
│   └── modal.py
├── tests/ui/
│   ├── conftest.py
│   ├── test_login.py
│   └── test_visual.py
├── utils/
│   └── api_helper.py         # API setup for UI tests
├── conftest.py
├── pytest.ini
└── requirements.txt</code></pre></div>""")

# ===== Ch4: pytest =====
write_html("pytest-fixtures.html", """<h3>Fixtures 深度用法</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">test_fixture_patterns.py</span></div>
<pre><code>import pytest


# 1. yield fixture — setup/teardown
@pytest.fixture
def db():
    conn = create_connection()
    yield conn      # test runs here
    conn.close()    # teardown


# 2. Fixture chaining
@pytest.fixture
def user(db):       # auto-depends on db
    u = db.insert_user("test")
    yield u
    db.delete_user(u.id)


# 3. Factory pattern — parameterizable creation
@pytest.fixture
def make_user(api):
    created = []
    def _create(name="test", role="user", **kw):
        u = api.create(name=name, role=role, **kw)
        created.append(u)
        return u
    yield _create
    for u in created: api.delete(u["id"])

def test_roles(make_user):
    admin = make_user(role="admin")
    viewer = make_user(role="viewer")</code></pre></div>""")

write_html("pytest-param.html", """<h3>参数化高级用法</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">test_param_advanced.py</span></div>
<pre><code>import pytest


# 1. Combinatorial — browser x viewport = 2x3 = 6 cases
@pytest.mark.parametrize("browser", ["chromium", "firefox"])
@pytest.mark.parametrize("viewport", ["desktop", "tablet", "mobile"])
def test_responsive(browser, viewport): pass


# 2. indirect — param goes to fixture
@pytest.fixture
def role(request): return create_user(role=request.param)

@pytest.mark.parametrize("role", ["admin","user","viewer"], indirect=True)
def test_permissions(role): pass  # role comes from fixture


# 3. Selective skip/xfail
@pytest.mark.parametrize("data,exp", [
    pytest.param({"n":"x"*300}, 422, marks=pytest.mark.skip(reason="Not live yet")),
    pytest.param({"n":"test"}, 201, id="Normal"),
])
def test_create(data, exp): pass</code></pre></div>""")

write_html("pytest-conftest.html", """<h3>conftest 层级管理</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">conftest hierarchy</span></div>
<pre><code># conftest.py               -> Root (CLI args, session fixtures)
# tests/conftest.py         -> Common (api client, db)
# tests/api/conftest.py     -> API-specific
# tests/ui/conftest.py      -> UI-specific (browser, page)
# tests/ui/order/conftest.py -> Order module specific
#
# Lookup: current dir -> parent -> ... -> root
# Child can override parent's fixture with same name</code></pre></div>""")

write_html("pytest-plugins.html", """<h3>插件生态</h3>
<table>
<tr><th>Plugin</th><th>Purpose</th><th>Level</th></tr>
<tr><td>pytest-xdist</td><td>Parallel (-n auto)</td><td><span class="badge b-green">Required</span></td></tr>
<tr><td>pytest-rerunfailures</td><td>Retry flaky tests</td><td><span class="badge b-green">Required</span></td></tr>
<tr><td>allure-pytest</td><td>Allure reports</td><td><span class="badge b-green">Required</span></td></tr>
<tr><td>pytest-timeout</td><td>Test timeout</td><td><span class="badge b-green">Recommended</span></td></tr>
<tr><td>pytest-order</td><td>Order control</td><td><span class="badge b-yellow">Optional</span></td></tr>
</table>""")

write_html("pytest-hooks.html", """<h3>Hook 机制</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">conftest.py</span></div>
<pre><code>def pytest_collection_modifyitems(config, items):
    '''Auto-tag tests based on path'''
    for item in items:
        if "api" in item.nodeid: item.add_marker(pytest.mark.api)
        elif "ui" in item.nodeid: item.add_marker(pytest.mark.ui)


def pytest_sessionfinish(session, exitstatus):
    if exitstatus != 0:
        print("\nReport: allure serve allure-results")</code></pre></div>""")

# ===== Ch5: CI/CD =====
write_html("ci-github.html", """<h3>GitHub Actions</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">.github/workflows/e2e-tests.yml</span></div>
<pre><code>name: E2E Tests
on:
  push: { branches: [main, develop] }
  pull_request: { branches: [main] }
  schedule: [{ cron: '0 3 * * *' }]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_DB: test, POSTGRES_PASSWORD: pass }
        ports: [5432:5432]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r backend/requirements.txt
      - run: pytest tests/test_api_*.py -v -n auto --alluredir=allure-results

  ui-tests:
    needs: api-tests
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix: { browser: [chromium, firefox] }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r backend/requirements.txt
      - run: playwright install --with-deps ${{ matrix.browser }}
      - run: pytest tests/test_ui_*.py --browser=${{ matrix.browser }} -v</code></pre></div>""")

write_html("ci-jenkins.html", """<h3>Jenkins Pipeline</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">Jenkinsfile</span></div>
<pre><code>pipeline {
    agent any
    parameters {
        choice(name: 'ENV', choices: ['staging', 'prod'])
        choice(name: 'SUITE', choices: ['smoke', 'regression'])
    }
    stages {
        stage('Setup') { steps { sh 'pip install -r backend/requirements.txt' } }
        stage('API') { steps { sh 'pytest tests/test_api_*.py -v -n auto' } }
        stage('UI') { steps { sh 'pytest tests/test_ui_*.py --browser=chromium -v' } }
    }
    post {
        failure { slackSend(channel: '#qa-alerts', message: 'Tests failed') }
    }
}</code></pre></div>""")

write_html("ci-docker.html", """<h3>Docker + Selenium Grid</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">docker-compose.yml</span></div>
<pre><code>services:
  app:
    build: .
    ports: ["8888:8888"]

  selenium-hub:
    image: selenium/hub:4
    ports: ["4444:4444"]

  chrome:
    image: selenium/node-chrome:4
    shm_size: '2gb'
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_NODE_MAX_SESSIONS=4</code></pre></div>""")

write_html("ci-allure.html", """<h3>Allure 报告发布到 GitHub Pages</h3>
<div class="cw"><div class="cbar"><span class="d d1"></span><span class="d d2"></span><span class="d d3"></span><span class="fname">.github/workflows/allure-report.yml</span></div>
<pre><code>name: Publish Allure
on:
  workflow_run:
    workflows: ["E2E Tests"]
    types: [completed]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
      - run: |
          pip install allure-combine
          allure-combine ./allure-results -o report
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./report</code></pre></div>""")

print(f"Generated module HTML files in {BASE}")
