from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
import jwt

app = FastAPI(title="Branches API", version="1.0.0")

# CORS Configuration - Allow requests from anywhere (including file://)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (including file:// for local HTML files)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Branch(BaseModel):
    branch_id: int
    branch_code: str
    branch_name: str
    type: str
    category: str
    country: str
    province: str
    city: str
    address: str
    contact: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

# Mock database
# Note: In production, ALWAYS use hashed passwords and a real database!
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin123",
        "disabled": False,
    }
}

branches_db = [
    {
        "branch_id": 1,
        "branch_code": "MATARAM",
        "branch_name": "Offline Mataram",
        "type": "Offline",
        "category": "Franchise",
        "country": "Indonesia",
        "province": "Nusa Tenggara Barat",
        "city": "Kota Mataram",
        "address": "Jl. Wr. Supratman No. 23, Mataram Timur",
        "contact": "081399649888"
    },
    {
        "branch_id": 2,
        "branch_code": "DENPASAR",
        "branch_name": "Offline Denpasar",
        "type": "Offline",
        "category": "Franchise",
        "country": "Indonesia",
        "province": "Bali",
        "city": "Denpasar",
        "address": "Jl. Teuku Umar No. 45, Denpasar",
        "contact": "081234567890"
    }
]

# Helper functions
def verify_password(plain_password, stored_password):
    return plain_password == stored_password

def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return user_dict
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("disabled"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Routes
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth 2.0 Token endpoint - Get access token
    
    Use this endpoint to get an access token by providing username and password.
    
    Default credentials:
    - username: admin
    - password: admin123
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/branches", response_model=List[Branch])
async def get_all_branches(current_user: dict = Depends(get_current_active_user)):
    """
    Get All Branches
    
    Returns a list of all branches. Requires valid OAuth 2.0 Bearer token.
    """
    return branches_db

@app.get("/")
async def root():
    """
    Welcome endpoint with API documentation
    """
    return {
        "message": "Branches API with OAuth 2.0",
        "documentation": "/docs",
        "endpoints": {
            "token": "POST /token - Get access token (username: admin, password: admin123)",
            "branches": "GET /api/branches - Get all branches (requires Bearer token)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
