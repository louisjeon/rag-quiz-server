-- Enable pgcrypto for UUID generation if not already enabled
create extension if not exists "pgcrypto";

create table if not exists public.users (
  id text primary key,
  email text unique,
  name text,
  picture text,
  created_at timestamptz not null default now()
);

create table if not exists public.quizzes (
  id uuid primary key default gen_random_uuid(),
  user_id text not null references public.users(id) on delete cascade,
  title text not null default 'Untitled Quiz',
  source_filename text,
  quizzes jsonb not null,
  created_at timestamptz not null default now()
);

create index if not exists quizzes_user_id_created_at_idx
  on public.quizzes(user_id, created_at desc);

