from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.questions import QuestionCreate, QuestionsResponse, AnswerCreate, QuestionBase

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

@router.get("/posts/u/{username}", response_model=QuestionsResponse)
async def get_user_posts(
    username: str, page: int = Query(1, ge=1), db: Session = Depends(get_db)
):
    questions, total = crud.get_questions_by_username(db, username)
    if not questions:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"questions": questions}

@router.get("/posts/{question_id}", response_model=QuestionBase)
async def get_specific_question(question_id: int, db: Session = Depends(get_db)):
    question = crud.get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return question

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
async def update_answer(answer_id: int, new_answer: AnswerCreate, db: SessionDep, user: CurrentUser):
    answer = crud.get_answer_by_id(db, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    if answer.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this answer")
    
    result = crud.update_answer_by_id(db, answer_id, new_answer.content)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to update answer")
    
    return {"message": "answer updated successfully"}

@router.delete("/answers/{answer_id}")
async def remove_answer(answer_id: int, db: SessionDep, user: CurrentUser):
    answer = crud.get_answer_by_id(db, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    
    if answer.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this answer")
    
    result = crud.remove_answer_by_id(db, answer_id)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to delete answer")
    
    return {"message": "answer deleted successfully"}