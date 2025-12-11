import asyncio
from typing import Any, Dict

from fastapi import Depends, HTTPException, Request, status
from supabase import Client, create_client

from .config import get_settings


def build_supabase_client() -> Client:
	settings = get_settings()
	if not settings.supabase_url or not settings.supabase_service_role_key:
		raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required")
	return create_client(settings.supabase_url, settings.supabase_service_role_key)


supabase_client: Client = build_supabase_client()


async def run_supabase(fn):
	"""Run blocking supabase client calls in a thread to avoid blocking the event loop."""
	return await asyncio.to_thread(fn)


def get_current_user(request: Request) -> Dict[str, Any]:
	user = request.session.get("user")
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
	return user


CurrentUser = Depends(get_current_user)

