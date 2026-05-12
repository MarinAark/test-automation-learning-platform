import os


class Settings:
    app_name: str = "测试开发学习平台"
    version: str = "1.0.0"
    env: str = os.getenv("ENV", "development")
    static_dir: str = os.path.join(os.path.dirname(__file__), "..", "frontend")
    cors_origins: list = ["*"]


settings = Settings()
