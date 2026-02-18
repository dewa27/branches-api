from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Branches API", version="2.0.0")

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuration ---
API_KEY = "775b22ab-01c7-4834-a8c8-df0cb0460c77"

# --- Models ---
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
    branches: List[int]  # Single row maps to multiple branch IDs
    name: str
    email: str
    phone: str
    birthday: str
    age: int
    npwp: str
    gender: str
    country: str
    province: str
    city: str
    address: str
    languages: List[str]
    skills: List[int]

class TeacherWithAuth(Teacher):
    username: str
    password_hash: str

class TeacherCreate(BaseModel):
    name: str
    email: str
    phone: str
    birthday: str
    age: int
    npwp: str
    gender: str
    country: str
    province: str
    city: str
    address: str
    languages: List[str]
    branches: List[int]

class TeacherCreateResponse(BaseModel):
    message: str
    teacher_id: int
    assigned_branches: List[int]

# --- Mock Database ---
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

skills_db = [
    {"skill_id": 1, "skill_name": "Python Game"},
    {"skill_id": 2, "skill_name": "Advanced Lua Coding with Roblox"},
    {"skill_id": 3, "skill_name": "Web Development"}
]

teachers_db = [
    {
        "teacher_id": 96,
        "name": "Budi Santoso",
        "email": "budi.santoso@email.com",
        "phone": "+6281122334455",
        "birthday": "12 May 1990",
        "age": 35,
        "npwp": "9988776655",
        "gender": "Male",
        "country": "Indonesia",
        "province": "DKI Jakarta",
        "city": "Jakarta Selatan",
        "address": "Jl. Kemang Raya No. 10",
        "languages": ["Indonesian", "English"],
        "branches": [1, 3],
        "skills": [1, 2],
        "username": "budi.santoso",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    },
    {
        "teacher_id": 97,
        "name": "Siti Aminah",
        "email": "siti.aminah@email.com",
        "phone": "+6281223344556",
        "birthday": "25 Aug 1993",
        "age": 32,
        "npwp": "8877665544",
        "gender": "Female",
        "country": "Indonesia",
        "province": "Jawa Barat",
        "city": "Bandung",
        "address": "Jl. Dago No. 45",
        "languages": ["Indonesian", "Sundanese"],
        "branches": [2],
        "skills": [1, 2],
        "username": "siti.aminah",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    },
    {
        "teacher_id": 98,
        "name": "I Wayan Putra",
        "email": "wayan.putra@email.com",
        "phone": "+6281334455667",
        "birthday": "03 Jan 1988",
        "age": 38,
        "npwp": "7766554433",
        "gender": "Male",
        "country": "Indonesia",
        "province": "Bali",
        "city": "Denpasar",
        "address": "Jl. Gatot Subroto No. 12",
        "languages": ["Indonesian", "Balinese", "English"],
        "branches": [2, 1],
        "skills": [1],
        "username": "wayan.putra",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    },
    {
        "teacher_id": 99,
        "name": "Dewi Lestari",
        "email": "dewi.lestari@email.com",
        "phone": "+6281445566778",
        "birthday": "14 Feb 1995",
        "age": 30,
        "npwp": "6655443322",
        "gender": "Female",
        "country": "Indonesia",
        "province": "Jawa Timur",
        "city": "Surabaya",
        "address": "Jl. Tunjungan No. 88",
        "languages": ["Indonesian", "Javanese"],
        "branches": [3],
        "skills": [3],
        "username": "dewi.lestari",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    },
    {
        "teacher_id": 100,
        "name": "Andi Wijaya",
        "email": "andi.wijaya@email.com",
        "phone": "+6281556677889",
        "birthday": "20 Nov 1992",
        "age": 33,
        "npwp": "5544332211",
        "gender": "Male",
        "country": "Indonesia",
        "province": "Nusa Tenggara Barat",
        "city": "Mataram",
        "address": "Jl. Pejanggik No. 5",
        "languages": ["Indonesian", "English"],
        "branches": [1],
        "skills": [1],
        "username": "andi.wijaya",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    },
    {
        "teacher_id": 101,
        "name": "Rina Kartika",
        "email": "rina.kartika@email.com",
        "phone": "+6281667788990",
        "birthday": "09 Jul 1997",
        "age": 28,
        "npwp": "4433221100",
        "gender": "Female",
        "country": "Indonesia",
        "province": "Banten",
        "city": "Tangerang",
        "address": "BSD City, Cluster Foresta",
        "languages": ["Indonesian", "English", "Mandarin"],
        "branches": [1, 2, 3],
        "skills": [1, 2, 3],
        "username": "rina.kartika",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    },
    {
        "teacher_id": 102,
        "name": "Eko Prasetyo",
        "email": "eko.prasetyo@email.com",
        "phone": "+6281778899001",
        "birthday": "30 Mar 1985",
        "age": 40,
        "npwp": "3322110099",
        "gender": "Male",
        "country": "Indonesia",
        "province": "DI Yogyakarta",
        "city": "Sleman",
        "address": "Jl. Kaliurang KM 5",
        "languages": ["Indonesian", "Javanese", "Dutch"],
        "branches": [2],
        "skills": [1, 2, 3],
        "username": "eko.prasetyo",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    },
    {
        "teacher_id": 103,
        "name": "Maya Sari",
        "email": "maya.sari@email.com",
        "phone": "+6281889900112",
        "birthday": "18 Dec 1994",
        "age": 31,
        "npwp": "2211009988",
        "gender": "Female",
        "country": "Indonesia",
        "province": "Sumatera Utara",
        "city": "Medan",
        "address": "Jl. S. Parman No. 202",
        "languages": ["Indonesian", "Hokkien"],
        "branches": [3, 1],
        "skills": [1, 2, 3],
        "username": "maya.sari",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    },
    {
        "teacher_id": 104,
        "name": "Rizky Fauzi",
        "email": "rizky.fauzi@email.com",
        "phone": "+6281990011223",
        "birthday": "05 Sep 1996",
        "age": 29,
        "npwp": "1100998877",
        "gender": "Male",
        "country": "Indonesia",
        "province": "Sulawesi Selatan",
        "city": "Makassar",
        "address": "Jl. Panakkukang No. 15",
        "languages": ["Indonesian", "Buginese"],
        "branches": [1],
        "skills": [1, 2, 3],
        "username": "rizky.fauzi",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    },
    {
        "teacher_id": 105,
        "name": "Lusi Natalia",
        "email": "lusi.natalia@email.com",
        "phone": "+6281001122334",
        "birthday": "24 Dec 1991",
        "age": 34,
        "npwp": "0099887766",
        "gender": "Female",
        "country": "Indonesia",
        "province": "Papua",
        "city": "Jayapura",
        "address": "Jl. Sentani No. 1",
        "languages": ["Indonesian", "English"],
        "branches": [2, 3],
        "skills": [1, 2, 3],
        "username": "lusi.natalia",
        "password_hash": "$2a$12$P98hyMR72X6QgLxnCbDy/O7Fd813a3pakVzjn4mEKBKKqhxt9KA/S"
    }
]
next_teacher_id = 106

# --- Dependency ---
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# --- Routes ---

@app.get("/")
async def root():
    return {
        "message": "Branches API v2.0.0",
        "auth": "Header: X-API-Key",
        "endpoints": {
            "GET /api/branches": "List all branches",
            "GET /api/teachers": "List all teachers (Admin/Auth data)",
            "POST /api/teachers": "Create one teacher assigned to many branches",
            "GET /api/branches/{id}/teachers": "Filter teachers by branch membership"
        }
    }

@app.get("/api/branches", response_model=List[Branch])
async def get_all_branches(x_api_key: str = Depends(verify_api_key)):
    return branches_db

@app.get("/api/branches/{branch_id}/teachers", response_model=List[Teacher])
async def get_teachers_by_branch(branch_id: int, x_api_key: str = Depends(verify_api_key)):
    if not any(b["branch_id"] == branch_id for b in branches_db):
        raise HTTPException(status_code=404, detail="Branch not found")
    
    # Filter: Return teacher if the branch_id exists in their branches list
    return [t for t in teachers_db if branch_id in t.get("branches", [])]

@app.get("/api/teachers", response_model=List[TeacherWithAuth])
async def get_all_teachers(x_api_key: str = Depends(verify_api_key)):
    return teachers_db

@app.get("/api/skills", response_model=List[Skill])
async def get_all_skills(x_api_key: str = Depends(verify_api_key)):
    return skills_db

@app.post("/api/teachers", response_model=TeacherCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(teacher: TeacherCreate, x_api_key: str = Depends(verify_api_key)):
    global next_teacher_id
    
    # Validation: Ensure all branch IDs provided exist
    valid_ids = {b["branch_id"] for b in branches_db}
    if not all(b_id in valid_ids for b_id in teacher.branches):
        raise HTTPException(status_code=404, detail="One or more Branch IDs not found")

    # Validation: Email uniqueness
    if any(t["email"] == teacher.email for t in teachers_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Single entry creation
    new_teacher = {
        "teacher_id": next_teacher_id,
        "branches": teacher.branches,
        "name": teacher.name,
        "email": teacher.email,
        "phone": teacher.phone,
        "birthday": teacher.birthday,
        "age": teacher.age,
        "npwp": teacher.npwp,
        "gender": teacher.gender,
        "country": teacher.country,
        "province": teacher.province,
        "city": teacher.city,
        "address": teacher.address,
        "languages": teacher.languages,
        "skills": []
    }
    
    teachers_db.append(new_teacher)
    
    res = {
        "message": "Teacher created successfully",
        "teacher_id": next_teacher_id,
        "assigned_branches": teacher.branches
    }
    
    next_teacher_id += 1
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)