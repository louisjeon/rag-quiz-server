# Backend (FastAPI + Supabase)

Google OAuth로 로그인한 사용자가 생성한 퀴즈(JSON)를 저장/조회하는 FastAPI 서버입니다. DB는 Supabase PostgreSQL을 사용합니다.

## 요구 사항

- Python 3.10+
- Supabase 프로젝트와 Service Role Key
- Google OAuth 클라이언트 (Redirect URI는 `http://localhost:5001/auth/callback` 등으로 설정)

## 설치 및 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # 값 채우기
uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

## 환경변수 (.env)

- `FASTAPI_SECRET_KEY` : 세션 쿠키 서명용 비밀키
- `SESSION_COOKIE_SECURE` / `SESSION_COOKIE_SAMESITE` / `SESSION_COOKIE_NAME`
- `FRONTEND_URL` : CORS 및 OAuth 로그인 성공 후 리다이렉트 대상
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`
- `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY`

## Supabase 스키마

`schema.sql` 실행:

```bash
psql "$SUPABASE_DB_URL" -f schema.sql
```

- `users(id, email, name, picture, created_at)`
- `quizzes(id, user_id, title, source_filename, quizzes jsonb, created_at)`

## 주요 API

- `GET /health` : 상태 체크
- `GET /auth/login` : 구글 로그인 시작 (쿠키 세션)
- `GET /auth/callback` : OAuth 콜백, Supabase `users` upsert, 세션 저장
- `POST /auth/logout` : 세션 삭제
- `GET /api/me` : 현재 세션 유저
- `GET /api/quizzes` : 내 퀴즈 목록
- `GET /api/quizzes/{id}` : 특정 퀴즈 조회
- `POST /api/quizzes` : 퀴즈 저장 (body는 `quizzes` 리스트 필수)

## 프런트엔드 연동 가이드

- CORS 허용 origin은 `FRONTEND_URL`
- 요청 시 `credentials: "include"` 로 쿠키 전달
- 생성된 퀴즈를 그대로 `POST /api/quizzes` body에 전달:

```json
{
  "title": "강의 1 요약 퀴즈",
  "source_filename": "lecture.pdf",
  "quizzes": [ ...QuizItem... ]
}
```

# rag-quiz-server
