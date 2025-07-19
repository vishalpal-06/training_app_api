from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TrainingBase(BaseModel):
    trainer: str
    topic: str
    training_datetime: datetime
    description: Optional[str] = None
    training_completed: Optional[bool] = False
    training_reschule_reason: Optional[str] = None  # renamed
    exam_inprogress: Optional[bool] = False         # changed from str to bool
    traing_logo_bs64: Optional[bytes] = None

class TrainingCreate(TrainingBase):
    pass


class TrainingUpdate(BaseModel):  # All fields optional for PATCH
    trainer: Optional[str] = None
    topic: Optional[str] = None
    training_datetime: Optional[datetime] = None
    description: Optional[str] = None
    training_completed: Optional[bool] = None
    training_reschule_reason: Optional[str] = None  # renamed
    exam_inprogress: Optional[bool] = None          # changed from str to bool
    traing_logo_bs64: Optional[bytes] = None


class TrainingOut(TrainingBase):
    training_id: int

    class Config:
        orm_mode = True
