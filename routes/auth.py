from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from utils.models import Employee
from utils.database import get_db

router = APIRouter(
    prefix='/employee-auth',
    tags=['Employee Auth']
)

# Constants
SECRET_KEY = 'your_employee_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="employee-auth/token")

# Token schema
class EmployeeToken(BaseModel):
    access_token: str
    token_type: str
    employee_data: dict

# Utility: Authenticate Employee
def authenticate_employee(username: str, password: str, db: Session):
    employee = db.query(Employee).filter(Employee.emailid == username).first()
    if not employee:
        return None
    #if not bcrypt_context.verify(password, employee.password):
    if not password == employee.password:
        return None
    return employee

# Utility: Create JWT token
def create_employee_access_token(emailid: str, employee_id: int, expires_delta: timedelta,training_team:bool):
    payload = {
        "sub": emailid,
        "employee_id": employee_id,
        "exp": datetime.now(timezone.utc) + expires_delta,
        "training_team": training_team
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Get Current Employee
async def get_current_employee(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        emailid: str = payload.get("sub")
        employee_id: int = payload.get("employee_id")
        training_team: int = payload.get("training_team")

        if emailid is None or employee_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return {"emailid": emailid, "employee_id": employee_id,"training_team": training_team}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Dependency
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_employee)]


# POST: Login route
@router.post("/token", response_model=EmployeeToken)
async def login_employee(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    employee = authenticate_employee(form_data.username, form_data.password, db)
    if not employee:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate employee")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_employee_access_token(employee.emailid, employee.employee_id, access_token_expires,employee.training_team)

    return {
        "access_token": token,
        "token_type": "bearer",
        "employee_data": {
            "employee_id": employee.employee_id,
            "emailid": employee.emailid,
            "employee_name": employee.employee_name,
            "training_team": employee.training_team,
            "manager_id": employee.manager_id,
            "is_manager": employee.is_manager,
        }
    }
