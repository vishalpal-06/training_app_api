from pydantic import BaseModel
from typing import Optional

class TrainingTestOut(BaseModel):
    question_id: int
    training_id: int
    question: str
    option1: str
    option2: str
    option3: str
    option4: str
    answer: str

    class Config:
        orm_mode = True


class AnswerCreate(BaseModel):
    question_id: int
    employee_id: int
    answer: Optional[str]

class AnswerOut(BaseModel):
    answer_id: int
    question_id: int
    employee_id: int
    answer: Optional[str]

    class Config:
        orm_mode = True