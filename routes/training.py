from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.database import get_db  # You need this function to get DB session
from utils import models
from schemas.training import TrainingCreate, TrainingUpdate, TrainingOut
from typing import List

router = APIRouter(
    prefix="/trainings",
    tags=["Trainings"]
)

# GET all
@router.get("/", response_model=List[TrainingOut])
def get_trainings(db: Session = Depends(get_db)):
    return db.query(models.Training).all()


# GET by ID
@router.get("/{training_id}", response_model=TrainingOut)
def get_training(training_id: int, db: Session = Depends(get_db)):
    training = db.query(models.Training).filter(models.Training.training_id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    return training


# CREATE
@router.post("/", response_model=TrainingOut)
def create_training(training: TrainingCreate, db: Session = Depends(get_db)):
    new_training = models.Training(**training.dict())
    db.add(new_training)
    db.commit()
    db.refresh(new_training)
    return new_training


# UPDATE
@router.put("/{training_id}", response_model=TrainingOut)
def update_training(training_id: int, updated_data: TrainingUpdate, db: Session = Depends(get_db)):
    training = db.query(models.Training).filter(models.Training.training_id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(training, key, value)
    
    db.commit()
    db.refresh(training)
    return training


# DELETE
@router.delete("/{training_id}")
def delete_training(training_id: int, db: Session = Depends(get_db)):
    training = db.query(models.Training).filter(models.Training.training_id == training_id).first()
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    
    db.delete(training)
    db.commit()
    return {"detail": "Training deleted successfully"}
