from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from utils.models import TrainingTest, Training
from .auth import get_current_employee,get_db
from schemas.training_test import TrainingTestOut
from io import BytesIO

router = APIRouter(prefix="/training_mcq_question", tags=["Training MCQ Question"])

@router.post("/upload-training-test/")
async def upload_training_test_excel(
    file: UploadFile = File(...),
    training_id: int = Form(...),
    db: Session = Depends(get_db),
    employee:Session = Depends(get_current_employee)
):
    # Validate training_id
    training = db.query(Training).filter(Training.training_id == training_id).first()
    if not training:
        raise HTTPException(status_code=400, detail=f"Training with ID {training_id} does not exist.")

    # Read Excel file
    try:
        # df = pd.read_excel(file.file)
        contents = await file.read()  # Read all file contents
        df = pd.read_excel(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading Excel file: {str(e)}")

    # Check required columns
    required_columns = ['question', 'option1', 'option2', 'option3', 'option4', 'correct_option']
    if not all(col in df.columns for col in required_columns):
        raise HTTPException(status_code=400, detail=f"Excel must contain columns: {', '.join(required_columns)}")

    # Insert rows into DB
    records_added = 0
    for _, row in df.iterrows():
        test = TrainingTest(
            training_id=training_id,
            question=row['question'],
            option1=row['option1'],
            option2=row['option2'],
            option3=row['option3'],
            option4=row['option4'],
            answer=row['correct_option']
        )
        db.add(test)
        records_added += 1

    db.commit()

    return {"message": f"{records_added} questions successfully added to training_id {training_id}"}



@router.delete("/delete-mcqs/{training_id}")
def delete_mcqs_by_training_id(training_id: int, db: Session = Depends(get_db), employee:Session = Depends(get_current_employee)):
    # Check if training exists
    training = db.query(Training).filter(Training.training_id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail=f"Training with ID {training_id} not found")

    # Delete all related MCQs
    deleted_count = db.query(TrainingTest).filter(TrainingTest.training_id == training_id).delete()
    db.commit()

    return {
        "message": f"Deleted {deleted_count} MCQs related to training_id {training_id}"
    }


@router.get("/questions/{training_id}", response_model=List[TrainingTestOut])
def get_questions_by_training_id(training_id: int, db: Session = Depends(get_db), employee:Session = Depends(get_current_employee)):
    # Optional: Check if training exists
    training = db.query(Training).filter(Training.training_id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail=f"Training with ID {training_id} not found")

    questions = db.query(TrainingTest).filter(TrainingTest.training_id == training_id).all()

    if not questions:
        raise HTTPException(status_code=404, detail=f"No questions found for training_id {training_id}")

    return questions