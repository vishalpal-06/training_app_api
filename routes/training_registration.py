from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .auth import get_db, get_current_employee
from utils.models import TrainingRegistration, Training
from schemas.training_registeration import TrainingRegistrationCreate, TrainingRegistrationUpdate, TrainingRegistrationOut

router = APIRouter(prefix="/training-registration", tags=["Training Registration"])


# Create registration
@router.post("/", response_model=TrainingRegistrationOut)
def create_registration(registration_data: TrainingRegistrationCreate, db: Session = Depends(get_db), employee:Session = Depends(get_current_employee)):
    # Check if the training_id exists
    training = db.query(Training).filter(Training.training_id == registration_data.training_id).first()
    if not training:
        raise HTTPException(status_code=400, detail=f"Training with ID {registration_data.training_id} does not exist.")

    # Proceed with registration creation
    registration = TrainingRegistration(**registration_data.dict())
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration


# Update registration
@router.put("/{registration_id}", response_model=TrainingRegistrationOut)
def update_registration(registration_id: int, updated_data: TrainingRegistrationUpdate, db: Session = Depends(get_db), employee:Session = Depends(get_current_employee)):
    registration = db.query(TrainingRegistration).filter(TrainingRegistration.registration_id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(registration, key, value)

    db.commit()
    db.refresh(registration)
    return registration


# Get single registration by ID
@router.get("/{registration_id}", response_model=TrainingRegistrationOut)
def get_registration(registration_id: int, db: Session = Depends(get_db), employee:Session = Depends(get_current_employee)):
    registration = db.query(TrainingRegistration).filter(TrainingRegistration.registration_id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    return registration


# Get all registrations
@router.get("/", response_model=List[TrainingRegistrationOut])
def get_all_registrations(db: Session = Depends(get_db), employee:Session = Depends(get_current_employee)):
    return db.query(TrainingRegistration).all()


# DELETE
@router.delete("/{registration_id}")
def delete_training(registration_id: int, db: Session = Depends(get_db), employee:Session = Depends(get_current_employee)):
    registration = db.query(TrainingRegistration).filter(TrainingRegistration.registration_id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    db.delete(registration)
    db.commit()
    return {"detail": "Registration deleted successfully"}