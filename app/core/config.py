from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Criativos Growth"
    anthropic_api_key: str = ""
    output_dir: str = "output"
    model: str = "claude-sonnet-4-20250514"

    class Config:
        env_file = ".env"


settings = Settings()
