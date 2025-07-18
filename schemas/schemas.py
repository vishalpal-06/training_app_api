from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TrainingBase(BaseModel):
    trainer: str
    topic: str
    training_datetime: datetime
    description: Optional[str] = None
    training_completed: Optional[bool] = False
    reason: Optional[str] = None
    exam_status: Optional[str] = "upcoming"
    traing_logo_bs64: Optional[bytes] = None


class TrainingCreate(TrainingBase):
    pass


class TrainingUpdate(TrainingBase):
    pass


class TrainingOut(TrainingBase):
    training_id: int

    class Config:
        orm_mode = True
