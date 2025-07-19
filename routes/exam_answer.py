from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.models import Answer, TrainingTest
from utils.database import get_db
from schemas.training_test import AnswerCreate, AnswerOut
from typing import List

router = APIRouter(prefix="/exam-QA", tags=["Training MCQ QA"])

@router.post("/answers/", response_model=AnswerOut)
def submit_answer(answer_data: AnswerCreate, db: Session = Depends(get_db)):
    # Check if the question exists
    question = db.query(TrainingTest).filter(TrainingTest.question_id == answer_data.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if answer already exists (optional: prevent duplicates)
    existing_answer = db.query(Answer).filter(
        Answer.question_id == answer_data.question_id,
        Answer.employee_id == answer_data.employee_id
    ).first()
    if existing_answer:
        raise HTTPException(status_code=400, detail="Answer already submitted")

    answer = Answer(**answer_data.dict())
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer



@router.get("/answers/{training_id}/{employee_id}", response_model=List[AnswerOut])
def get_answers_by_training_and_employee(training_id: int, employee_id: int, db: Session = Depends(get_db)):
    # Get all question_ids for the training
    questions = db.query(TrainingTest.question_id).filter(TrainingTest.training_id == training_id).all()
    question_ids = [q.question_id for q in questions]

    # Fetch answers for those questions and the given employee
    answers = db.query(Answer).filter(
        Answer.question_id.in_(question_ids),
        Answer.employee_id == employee_id
    ).all()

    if not answers:
        raise HTTPException(status_code=404, detail="No answers found")

    return answers