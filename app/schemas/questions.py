from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.schemas.user import UserBase

class AnswerBase(BaseModel):
    id: int
    content: str
    created_at: datetime

class AnswerCreate(BaseModel):
    content: str

class QuestionBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    content: str
    created_at: datetime
    is_anonymous: bool
    answers: list[AnswerBase]
    user: UserBase = Field(alias="answerer")


class QuestionCreate(BaseModel):
    to_user_id: int
    isAnonymous: bool
    question: str

class QuestionsResponse(BaseModel):
    questions: list[QuestionBase]

