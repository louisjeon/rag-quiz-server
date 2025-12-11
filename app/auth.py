from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from .config import get_settings
from .deps import CurrentUser, run_supabase, supabase_client

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


def verify_id_token(token: str) -> Dict[str, Any]:
	if not settings.google_client_id:
		raise HTTPException(status_code=500, detail="Google client id not configured")
	try:
		return id_token.verify_oauth2_token(
			token,
			google_requests.Request(),
			audience=settings.google_client_id,
		)
	except Exception as exc:
		raise HTTPException(status_code=401, detail=f"Invalid id_token: {exc}") from exc


@router.post("/token")
async def auth_with_token(body: Dict[str, str], request: Request):
	token = body.get("id_token")
	if not token:
		raise HTTPException(status_code=400, detail="id_token is required")

	userinfo = verify_id_token(token)
	if "sub" not in userinfo:
		raise HTTPException(status_code=400, detail="Invalid user info")

	user_payload = {
		"id": userinfo["sub"],
		"email": userinfo.get("email"),
		"name": userinfo.get("name"),
		"picture": userinfo.get("picture"),
	}

	await run_supabase(lambda: supabase_client.table("users").upsert(user_payload).execute())

	request.session["user"] = user_payload
	return {"user": user_payload}


@router.post("/logout")
async def auth_logout(request: Request):
	request.session.clear()
	return {"ok": True}


@router.get("/me")
async def api_me(user: CurrentUser):
	return {"user": user}

