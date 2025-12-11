from typing import List, Optional

from pydantic import BaseModel, Field


class QuizItem(BaseModel):
	question: str
	options: Optional[List[str]] = None
	answer: str
	explanation: Optional[str] = None
	difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")


class QuizCreate(BaseModel):
	title: Optional[str] = "Untitled Quiz"
	source_filename: Optional[str] = None
	quizzes: List[QuizItem]

	class Config:
		json_schema_extra = {
			"example": {
				"title": "강의 1 요약 퀴즈",
				"source_filename": "lecture1.pdf",
				"quizzes": [
					{
						"question": "예시 질문?",
						"options": ["A", "B", "C", "D"],
						"answer": "A",
						"explanation": "정답 설명",
						"difficulty": "easy",
					}
				],
			}
		}

