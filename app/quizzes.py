from fastapi import APIRouter, Depends, HTTPException, status

from .deps import CurrentUser, run_supabase, supabase_client
from .schemas import QuizCreate

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])


@router.get("")
async def list_quizzes(user: CurrentUser):
	resp = await run_supabase(
		lambda: supabase_client.table("quizzes")
		.select("*")
		.eq("user_id", user["id"])
		.order("created_at", desc=True)
		.execute()
	)
	return {"quizzes": resp.data}


@router.get("/{quiz_id}")
async def get_quiz(quiz_id: str, user: CurrentUser):
	resp = await run_supabase(
		lambda: supabase_client.table("quizzes")
		.select("*")
		.eq("id", quiz_id)
		.eq("user_id", user["id"])
		.single()
		.execute()
	)
	if not resp.data:
		raise HTTPException(status_code=404, detail="Not found")
	return resp.data


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_quiz(payload: QuizCreate, user: CurrentUser):
	if not payload.quizzes:
		raise HTTPException(status_code=400, detail="quizzes must be non-empty")

	record = {
		"user_id": user["id"],
		"title": payload.title or "Untitled Quiz",
		"source_filename": payload.source_filename,
		"quizzes": [quiz.model_dump() for quiz in payload.quizzes],
	}

	resp = await run_supabase(lambda: supabase_client.table("quizzes").insert(record).execute())
	return resp.data[0]

