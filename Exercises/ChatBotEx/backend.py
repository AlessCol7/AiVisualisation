# # backend.py
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from pydantic import BaseModel
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# import socketio


# DATABASE_URL = "sqlite:///./chat.db"
# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
# app = FastAPI()
# socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# Base = declarative_base()
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     hashed_password = Column(String)

# Base.metadata.create_all(bind=engine)

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
# )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# class UserCredentials(BaseModel):
#     username: str
#     password: str

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# @app.post("/register")
# def register(credentials: UserCredentials, db: Session = Depends(get_db)):
#     if db.query(User).filter(User.username == credentials.username).first():
#         raise HTTPException(status_code=400, detail="Username already registered")
#     user = User(username=credentials.username, hashed_password=get_password_hash(credentials.password))
#     db.add(user)
#     db.commit()
#     return {"msg": "User registered"}

# @app.post("/login")
# def login(credentials: UserCredentials, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == credentials.username).first()
#     if not user or not verify_password(credentials.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid username or password")
#     token = create_access_token({"sub": credentials.username})
#     return {"access_token": token}


from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import shutil
import os
import socketio

# === CONFIG ===
DATABASE_URL = "sqlite:///./chat.db"
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
UPLOAD_DIR = "uploaded_files"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# === SOCKET.IO & FASTAPI APP ===
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
app = FastAPI()
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

# === DATABASE SETUP ===
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# === PASSWORD HASHING ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === MODELS ===
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

# === CORS MIDDLEWARE ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === DEPENDENCY ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === SCHEMAS ===
class UserCredentials(BaseModel):
    username: str
    password: str

# === UTILS ===
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# === ROUTES ===

@app.post("/register")
def register(credentials: UserCredentials, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == credentials.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(username=credentials.username, hashed_password=get_password_hash(credentials.password))
    db.add(user)
    db.commit()
    return {"msg": "User registered"}

@app.post("/login")
def login(credentials: UserCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": credentials.username})
    return {"access_token": token}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return {"filename": file.filename, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
