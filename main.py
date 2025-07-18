from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import engine
import utils.models as models

app = FastAPI(
    title="Training Management API",
    description="API to manage employee training sessions, including registration, session scheduling, and attendance tracking.",
    version="1.0.0",
)


origins = [
    "http://localhost:3000",
]

# Allow frontend (React) to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health/")
def heath_check():
    return {"Status":"Healthy"}


models.Base.metadata.create_all(bind=engine)