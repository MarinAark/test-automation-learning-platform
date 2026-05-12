"""全局测试配置"""
import pytest
import sys
import os

# 将项目根目录加入 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pytest_addoption(parser):
    parser.addoption("--browser", default="chromium", choices=["chromium", "firefox", "webkit"])
    parser.addoption("--headed", action="store_true")
    parser.addoption("--base-url", default="http://localhost:8888")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, "rep_" + outcome.get_result().when, outcome.get_result())
