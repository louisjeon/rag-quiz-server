import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
	frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
	fastapi_secret_key: str = os.getenv("FASTAPI_SECRET_KEY", "dev-secret-change-me")
	session_cookie_name: str = os.getenv("SESSION_COOKIE_NAME", "quiz_session")
	session_cookie_samesite: str = os.getenv("SESSION_COOKIE_SAMESITE", "lax")
	session_cookie_secure: bool = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"

	supabase_url: str | None = os.getenv("SUPABASE_URL")
	supabase_service_role_key: str | None = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

	google_client_id: str | None = os.getenv("GOOGLE_CLIENT_ID")
	google_client_secret: str | None = os.getenv("GOOGLE_CLIENT_SECRET")


@lru_cache
def get_settings() -> Settings:
	return Settings()

