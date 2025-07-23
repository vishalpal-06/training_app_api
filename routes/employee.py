from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.models import Employee  
from .auth import get_db, get_current_employee
from schemas.employee import EmployeeOut 

router = APIRouter(tags=["Employee Management"], prefix="/employee")

@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee_by_id(employee_id: int, db: Session = Depends(get_db), user: Session = Depends(get_current_employee)):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
