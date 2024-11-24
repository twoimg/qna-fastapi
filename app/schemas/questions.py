from pydantic import BaseModel
from datetime import datetime

class AnswerBase(BaseModel):
    id: int
    content: str
    created_at: datetime

class AnswerCreate(BaseModel):
    content: str

class QuestionBase(BaseModel):
    id: int
    content: str
    created_at: datetime
    is_anonymous: bool
    answers: list[AnswerBase]


class QuestionCreate(BaseModel):
    to_user_id: int
    isAnonymous: bool
    question: str

class QuestionsResponse(BaseModel):
    questions: list[QuestionBase]

