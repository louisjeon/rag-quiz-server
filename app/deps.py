import asyncio
from typing import Annotated, Any, Dict

import httpx
import gotrue.http_clients as gotrue_http_clients
import gotrue._sync.gotrue_base_api as gotrue_base_api
from fastapi import Depends, HTTPException, Request, status
from supabase import Client, create_client

from .config import get_settings


# Work around gotrue -> httpx proxy arg mismatch (gotrue passes proxy, httpx expects proxies)
class _PatchedSyncClient(httpx.Client):
	def __init__(self, *args, proxy=None, **kwargs):
		if proxy:
			kwargs["proxies"] = proxy
		super().__init__(*args, **kwargs)

	def aclose(self) -> None:
		self.close()


# Patch both the shared http_clients module and the already-imported reference inside gotrue_base_api
gotrue_http_clients.SyncClient = _PatchedSyncClient
gotrue_base_api.SyncClient = _PatchedSyncClient


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


CurrentUser = Annotated[Dict[str, Any], Depends(get_current_user)]

