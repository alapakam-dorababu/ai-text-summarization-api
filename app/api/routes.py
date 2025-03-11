from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlmodel import Session, select
from app.db.models import User
from app.db.database import get_db
from app.core.security import create_access_token, pwd_context
from app.services.auth import get_current_user
from app.services.summarization import (
    summarize_text,
    summarize_pdf,
    summarize_docx,
    summarize_url,
)
from app.dependencies.rate_limiter import rate_limiter
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register")
async def register(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.exec(select(User).where(User.username == username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.exec(select(User).where(User.username == form_data.username)).first()

    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/private")
@rate_limiter(limit=10, period=10, unit="minutes")
async def private_route(request: Request, user: User = Depends(get_current_user)):
    return {"message": f"API Authentication access granted for {user.username}."}


@router.post("/summarize/text/")
def summarize_text_endpoint(request: str):
    return {"summary": summarize_text(request)}


@router.post("/summarize/pdf/")
async def summarize_pdf_endpoint(file: UploadFile = File(...)):
    return {"summary": summarize_pdf(file)}


@router.post("/summarize/docx/")
async def summarize_docx_endpoint(file: UploadFile = File(...)):
    return {"summary": summarize_docx(file)}


@router.post("/summarize/url/")
async def summarize_url_endpoint(request: str):
    return {"summary": summarize_url(request)}
