# Application settings loaded from environment variables / .env file.
#
# Uses pydantic-settings (BaseSettings).
#
# Fields:
#   - ANTHROPIC_API_KEY: str         — Claude API key
#   - CLAUDE_MODEL: str              — model ID, e.g. "claude-sonnet-4-6"
#   - CORS_ORIGINS: list[str]        — allowed origins for CORS
#   - ENV: str                       — "development" | "production"
#
# A single `get_settings()` function cached with @lru_cache is exported
# and injected via FastAPI Depends() wherever config is needed.
