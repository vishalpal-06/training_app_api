from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TrainingRegistrationBase(BaseModel):
    training_id: int
    employee_id: int
    manager_id: int
    training_request: bool
    approval: bool
    registration_datetime: datetime
    reject_reason: Optional[str] = None


class TrainingRegistrationCreate(TrainingRegistrationBase):
    pass


class TrainingRegistrationUpdate(BaseModel):  # all optional for update
    training_id: Optional[int] = None
    employee_id: Optional[int] = None
    manager_id: Optional[int] = None
    training_request: Optional[bool] = None
    approval: Optional[bool] = None
    registration_datetime: Optional[datetime] = None
    reject_reason: Optional[str] = None


class TrainingRegistrationOut(TrainingRegistrationBase):
    registration_id: int

    class Config:
        orm_mode = True
