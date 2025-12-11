from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse

from app import auth, quizzes
from app.config import get_settings

settings = get_settings()

app = FastAPI()

app.add_middleware(
	SessionMiddleware,
	secret_key=settings.fastapi_secret_key,
	session_cookie=settings.session_cookie_name,
	same_site=settings.session_cookie_samesite,
	https_only=settings.session_cookie_secure,
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=[settings.frontend_url],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/health")
async def health():
	return {"status": "ok"}


app.include_router(auth.router)
app.include_router(quizzes.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(_, exc: Exception):
	return JSONResponse(
		status_code=500,
		content={"error": "Internal Server Error", "detail": str(exc)},
	)

