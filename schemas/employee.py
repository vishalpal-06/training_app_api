from pydantic import BaseModel
from typing import Optional

class EmployeeOut(BaseModel):
    employee_id: int
    employee_no: str
    employee_name: str
    emailid: str
    manager_id: Optional[int]
    team_id: int
    grade_id: Optional[int]
    discontinued: bool
    training_team: bool

    class Config:
        orm_mode = True
