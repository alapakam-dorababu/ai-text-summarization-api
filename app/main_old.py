# import jwt
# from typing import Optional
# from datetime import datetime, timedelta

# from pydantic import BaseModel
# from passlib.context import CryptContext
# from sqlmodel import SQLModel, Session, create_engine, select

# from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Depends
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# from app.services.summarization import summarize_text
# from app.utils.extractors import (
#     extract_text_from_pdf,
#     extract_text_from_docx,
#     extract_text_from_url,
# )
# from .dependencies import rate_limiter

# # Database setup
# DATABASE_URL = "sqlite:///users.db"  # Change to PostgreSQL/MySQL if needed
# engine = create_engine(DATABASE_URL, echo=True)

# # JWT setup
# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Password hashing context
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# from sqlmodel import SQLModel, Field


# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)  # Explicit Primary Key
#     username: str = Field(unique=True, index=True)  # Ensuring uniqueness
#     hashed_password: str


# # Pydantic Models
# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class RegisterRequest(BaseModel):
#     username: str
#     password: str


# class UserResponse(BaseModel):
#     id: int
#     username: str


# # Database initialization
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_db():
#     """Dependency to get database session"""
#     with Session(engine) as session:
#         yield session


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     """Generate a JWT access token"""
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (
#         expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# def verify_token(token: str):
#     """Decode and verify JWT token"""
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# async def get_current_user(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
# ):
#     """Retrieve current user from JWT token"""
#     payload = verify_token(token)
#     username: str = payload.get("sub")

#     user = db.exec(select(User).where(User.username == username)).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid token user")

#     return user


# app = FastAPI(on_startup=[create_db_and_tables])


# @app.post("/register", response_model=UserResponse)
# async def register(user: RegisterRequest, db: Session = Depends(get_db)):
#     """Register a new user"""
#     existing_user = db.exec(select(User).where(User.username == user.username)).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")

#     hashed_password = pwd_context.hash(user.password)
#     new_user = User(username=user.username, hashed_password=hashed_password)

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


# @app.post("/token", response_model=Token)
# async def login(
#     form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
# ):
#     """Login endpoint to generate JWT tokens"""
#     user = db.exec(select(User).where(User.username == form_data.username)).first()

#     if not user or not pwd_context.verify(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Invalid username or password")

#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/private")
# @rate_limiter(limit=10, period=10, unit="minutes")
# async def private_route(request: Request, user: User = Depends(get_current_user)):
#     """
#     Private API route with authentication and rate limiting.

#     - Requires a valid Bearer token.
#     - Enforces a rate limit (10 requests per 10 minutes).
#     - Returns a success message if within the allowed limit.
#     """
#     return {"message": f"API Authentication access granted for {user.username}."}


# @app.post("/summarize/text/")
# def summarize_text_endpoint(request: str):
#     if not request.strip():
#         raise HTTPException(status_code=400, detail="Text cannot be empty")
#     return {"summary": summarize_text(request)}


# @app.post("/summarize/pdf/")
# async def summarize_pdf(file: UploadFile = File(...)):
#     text = extract_text_from_pdf(file)
#     return {"summary": summarize_text(text)}


# @app.post("/summarize/docx/")
# async def summarize_docx(file: UploadFile = File(...)):
#     text = extract_text_from_docx(file)
#     return {"summary": summarize_text(text)}


# @app.post("/summarize/url/")
# async def summarize_url(request: str):
#     text = extract_text_from_url(request)
#     return {"summary": summarize_text(text)}
