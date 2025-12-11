from typing import Any, Dict, Optional

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, HTTPException, Request, status
from starlette.responses import RedirectResponse

from .config import get_settings
from .deps import CurrentUser, run_supabase, supabase_client

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

oauth = OAuth()
oauth.register(
	"google",
	client_id=settings.google_client_id,
	client_secret=settings.google_client_secret,
	server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
	client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def auth_login(request: Request):
	redirect_uri = request.url_for("auth_callback")
	return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def auth_callback(request: Request):
	token = await oauth.google.authorize_access_token(request)
	userinfo: Optional[Dict[str, Any]] = token.get("userinfo")

	if not userinfo:
		resp = await oauth.google.get("userinfo", token=token)
		userinfo = resp.json()

	if not userinfo or "sub" not in userinfo:
		raise HTTPException(status_code=400, detail="Failed to fetch user info")

	user_payload = {
		"id": userinfo["sub"],
		"email": userinfo.get("email"),
		"name": userinfo.get("name"),
		"picture": userinfo.get("picture"),
	}

	await run_supabase(lambda: supabase_client.table("users").upsert(user_payload).execute())

	request.session["user"] = user_payload
	return RedirectResponse(url=settings.frontend_url, status_code=status.HTTP_302_FOUND)


@router.post("/logout")
async def auth_logout(request: Request):
	request.session.clear()
	return {"ok": True}


@router.get("/me")
async def api_me(user: CurrentUser):
	return {"user": user}

