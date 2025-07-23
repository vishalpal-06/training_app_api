from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from .auth import get_db, get_current_employee
from utils.models import TrainingRegistration, Training
from schemas.training_registeration import TrainingRegistrationCreate, TrainingRegistrationUpdate, TrainingRegistrationOut

router = APIRouter(prefix="/training-registration-manager", tags=["Manager Registration"])

# Get single registration by ID
@router.get("/{manager_id}", response_model=List[TrainingRegistrationOut])
def get_registration_manager(manager_id: int, db: Session = Depends(get_db), employee:Session = Depends(get_current_employee)):
    registration = db.query(TrainingRegistration).filter(TrainingRegistration.manager_id == manager_id).all()
    # if not registration:
    #     raise HTTPException(status_code=404, detail="Registration not found")
    return registration


# Get all registrations
@router.get("/", response_model=List[TrainingRegistrationOut])
def get_all_registrations(db: Session = Depends(get_db), employee:Session = Depends(get_current_employee)):
    return db.query(TrainingRegistration).all()

