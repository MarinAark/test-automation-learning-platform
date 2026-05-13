from datetime import datetime, timedelta
import random

from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/reports", tags=["reports"])

random.seed(42)


@router.get("/overview")
async def get_overview():
    """聚合统计数据 — 模拟最近 30 天的测试执行概况"""
    total_runs = 2847
    passed = 2618
    failed = total_runs - passed
    pass_rate = round(passed / total_runs * 100, 1)

    # 最近 7 天趋势
    days = []
    now = datetime.now()
    for i in range(6, -1, -1):
        d = now - timedelta(days=i)
        runs = random.randint(70, 130)
        p = random.randint(int(runs * 0.82), runs)
        days.append({
            "date": d.strftime("%m/%d"),
            "runs": runs,
            "passed": p,
            "failed": runs - p,
            "avg_duration": round(random.uniform(2.1, 6.8), 1),
        })

    return {
        "total_runs": total_runs,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "avg_duration": "3.2s",
        "total_suites": 42,
        "flaky_count": 23,
        "trend": days,
    }


@router.get("/failures")
async def get_failures():
    """失败原因分布"""
    categories = [
        {"name": "元素定位失败", "count": 87, "color": "#ef4444"},
        {"name": "断言失败", "count": 64, "color": "#f97316"},
        {"name": "超时", "count": 41, "color": "#f59e0b"},
        {"name": "环境问题", "count": 23, "color": "#8b5cf6"},
        {"name": "数据问题", "count": 14, "color": "#3b82f6"},
    ]
    total = sum(c["count"] for c in categories)
    for c in categories:
        c["percentage"] = round(c["count"] / total * 100, 1)
    return {"categories": categories, "total_failures": total}


@router.get("/history")
async def get_history(limit: int = Query(10, ge=1, le=50)):
    """最近执行历史"""
    envs = ["staging", "production", "preview", "dev"]
    triggers = ["定时触发", "PR #{}", "手动触发", "Webhook"]
    entries = []
    now = datetime.now()
    for i in range(limit):
        d = now - timedelta(hours=i * 3 + random.randint(0, 8))
        runs = random.randint(40, 150)
        p = random.randint(int(runs * 0.85), runs)
        entries.append({
            "id": f"run-{1000 + i}",
            "time": d.strftime("%Y-%m-%d %H:%M"),
            "env": random.choice(envs),
            "trigger": random.choice(triggers).format(random.randint(100, 999)),
            "total": runs,
            "passed": p,
            "failed": runs - p,
            "skipped": random.randint(0, 3),
            "duration": f"{random.randint(1, 8)}m {random.randint(10, 55)}s",
            "pass_rate": round(p / runs * 100, 1),
            "report_url": "#",
        })
    entries.sort(key=lambda e: e["time"], reverse=True)
    return {"history": entries}
