from fastapi import APIRouter, Depends, HTTPException

from app.schemas.questions import QuestionCreate, QuestionsResponse, AnswerCreate

from app.core.database.db import get_db
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import CurrentUser, SessionDep

router = APIRouter()

@router.post("/posts")
async def post_query(question: QuestionCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, question.to_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    question = crud.create_question(db, question)
    
    return {"message": "query posted"}

@router.get("/posts/{user_id}/", response_model=QuestionsResponse)
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    questions = crud.get_questions_by_user_id(db, user_id)
    return {"questions": questions}

@router.get("/posts/{question_id}")
async def get_specific_question(question_id: int, db: Session = Depends(get_db)):
    question = crud.get_question_by_id(db, question_id)
    return {"question": question}

@router.post("/posts/{question_id}/answers")
async def answer_question(
    question_id: int, answer: AnswerCreate, user: CurrentUser, db: SessionDep
):
    question = crud.get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    answer = crud.create_answer(db, question_id, user.id, answer)
    return {"message": "posted question answer"}

@router.put("/answers/{answer_id}")
async def update_answer(answer_id: int):
    return {"message": "update question answer"}

@router.delete("/answers/{answer_id}")
async def remove_answer(answer_id: int):
    return {"message": "removed answer"}