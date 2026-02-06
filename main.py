from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Branches API", version="2.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
API_KEY = "eaae442e-7560-4158-9665-2f0d27c7a082"  # Change this to a secure API key

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

class Skill(BaseModel):
    skill_id: int
    skill_name: str

class Teacher(BaseModel):
    teacher_id: int
    name: str
    email: str
    phone: str
    birthday: str
    age: int
    npwp: str
    gender: str
    region: str
    address: str
    languages: List[str]
    skills: List[Skill]

class TeacherCreate(BaseModel):
    name: str
    email: str
    phone: str
    birthday: str
    age: int
    npwp: str
    gender: str
    region: str
    address: str
    languages: List[str]
    additional_branches: Optional[List[int]] = []

class TeacherCreateResponse(BaseModel):
    message: str
    teacher_id: int
    assigned_branches: List[int]

# Mock Database
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
    },
    {
        "branch_id": 3,
        "branch_code": "JAKARTA",
        "branch_name": "Offline Jakarta",
        "type": "Offline",
        "category": "Corporate",
        "country": "Indonesia",
        "province": "DKI Jakarta",
        "city": "Jakarta Selatan",
        "address": "Jl. Sudirman No. 123",
        "contact": "081234567891"
    }
]

skills_db = [
    {
        "skill_id": 1,
        "skill_name": "Python Game"
    },
    {
        "skill_id": 2,
        "skill_name": "Advanced Lua Coding with Roblox"
    },
    {
        "skill_id": 3,
        "skill_name": "Web Development"
    },
    {
        "skill_id": 4,
        "skill_name": "Mobile App Development"
    }
]

teachers_db = [
    {
        "teacher_id": 101,
        "branch_id": 1,
        "name": "Lalu Rudi Setiawan",
        "email": "rudistiawannn@gmail.com",
        "phone": "+6281938587824",
        "birthday": "14 Nov 2001",
        "age": 24,
        "npwp": "1234567890",
        "gender": "Male",
        "region": "Kota Mataram, Nusa Tenggara Barat, Indonesia",
        "address": "Mangkung, Lombok Tengah",
        "languages": ["Indonesian", "English"],
        "skills": [
            {
                "skill_id": 1,
                "skill_name": "Python Game"
            }
        ]
    },
    {
        "teacher_id": 102,
        "branch_id": 1,
        "name": "Ani Susanti",
        "email": "ani.susanti@gmail.com",
        "phone": "+6281234567890",
        "birthday": "10 May 1998",
        "age": 26,
        "npwp": "0987654321",
        "gender": "Female",
        "region": "Kota Mataram, Nusa Tenggara Barat, Indonesia",
        "address": "Cakranegara, Mataram",
        "languages": ["Indonesian", "English"],
        "skills": [
            {
                "skill_id": 2,
                "skill_name": "Advanced Lua Coding with Roblox"
            }
        ]
    },
    {
        "teacher_id": 103,
        "branch_id": 2,
        "name": "Made Wirawan",
        "email": "made.wirawan@gmail.com",
        "phone": "+6281345678901",
        "birthday": "05 Aug 2000",
        "age": 25,
        "npwp": "1122334455",
        "gender": "Male",
        "region": "Denpasar, Bali, Indonesia",
        "address": "Denpasar Selatan",
        "languages": ["Indonesian", "English", "Balinese"],
        "skills": [
            {
                "skill_id": 3,
                "skill_name": "Web Development"
            }
        ]
    }
]

# Counter for new teacher IDs
next_teacher_id = 104

# API Key Authentication
async def verify_api_key(x_api_key: str = Header(...)):
    """
    Verify API Key from header
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return x_api_key

# Routes
@app.get("/")
async def root():
    """
    Welcome endpoint with API documentation
    """
    return {
        "message": "Branches API with API Key Authentication",
        "version": "2.0.0",
        "documentation": "/docs",
        "authentication": "Use header: X-API-Key: your-api-key-here",
        "endpoints": {
            "branches": "GET /api/branches - Get all branches",
            "teachers_by_branch": "GET /api/branches/{branch_id}/teachers - Get teachers by branch",
            "skills": "GET /api/skills - Get all skills",
            "create_teacher": "POST /api/branches/{branch_id}/teachers - Create new teacher"
        }
    }

@app.get("/api/branches", response_model=List[Branch])
async def get_all_branches(x_api_key: str = Depends(verify_api_key)):
    """
    Get All Branches
    
    Returns a list of all branches. Requires valid API Key in X-API-Key header.
    """
    return branches_db

@app.get("/api/branches/{branch_id}/teachers", response_model=List[Teacher])
async def get_teachers_by_branch(branch_id: int, x_api_key: str = Depends(verify_api_key)):
    """
    Get Teachers by Branch ID
    
    Returns a list of teachers assigned to the specified branch.
    Requires valid API Key in X-API-Key header.
    """
    # Check if branch exists
    branch_exists = any(branch["branch_id"] == branch_id for branch in branches_db)
    if not branch_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch with ID {branch_id} not found"
        )
    
    # Get teachers for this branch
    teachers = [teacher for teacher in teachers_db if teacher["branch_id"] == branch_id]
    
    if not teachers:
        return []
    
    return teachers

@app.get("/api/skills", response_model=List[Skill])
async def get_all_skills(x_api_key: str = Depends(verify_api_key)):
    """
    Get All Skills
    
    Returns a list of all available skills.
    Requires valid API Key in X-API-Key header.
    """
    return skills_db

@app.post("/api/branches/{branch_id}/teachers", response_model=TeacherCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(branch_id: int, teacher: TeacherCreate, x_api_key: str = Depends(verify_api_key)):
    """
    Create Teacher to Branch
    
    Creates a new teacher and assigns them to the specified branch.
    Optionally assign to additional branches.
    Requires valid API Key in X-API-Key header.
    """
    global next_teacher_id
    
    # Check if branch exists
    branch_exists = any(branch["branch_id"] == branch_id for branch in branches_db)
    if not branch_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch with ID {branch_id} not found"
        )
    
    # Check if additional branches exist
    if teacher.additional_branches:
        for add_branch_id in teacher.additional_branches:
            branch_exists = any(branch["branch_id"] == add_branch_id for branch in branches_db)
            if not branch_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Additional branch with ID {add_branch_id} not found"
                )
    
    # Check if email already exists
    email_exists = any(t["email"] == teacher.email for t in teachers_db)
    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teacher with this email already exists"
        )
    
    # Create new teacher for primary branch
    new_teacher = {
        "teacher_id": next_teacher_id,
        "branch_id": branch_id,
        "name": teacher.name,
        "email": teacher.email,
        "phone": teacher.phone,
        "birthday": teacher.birthday,
        "age": teacher.age,
        "npwp": teacher.npwp,
        "gender": teacher.gender,
        "region": teacher.region,
        "address": teacher.address,
        "languages": teacher.languages,
        "skills": []  # Will be empty for new teachers, can be updated later
    }
    
    teachers_db.append(new_teacher)
    
    # Create entries for additional branches (same teacher, different branch_id)
    assigned_branches = [branch_id]
    if teacher.additional_branches:
        for add_branch_id in teacher.additional_branches:
            additional_teacher = new_teacher.copy()
            additional_teacher["branch_id"] = add_branch_id
            teachers_db.append(additional_teacher)
            assigned_branches.append(add_branch_id)
    
    response = {
        "message": "Teacher created successfully",
        "teacher_id": next_teacher_id,
        "assigned_branches": assigned_branches
    }
    
    next_teacher_id += 1
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
