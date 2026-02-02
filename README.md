# Branches API with OAuth 2.0

A simple FastAPI application with OAuth 2.0 Bearer token authentication for managing branch data.

## Features

- ✅ OAuth 2.0 Password Flow (Bearer Token)
- ✅ JWT Token-based authentication
- ✅ Password hashing with bcrypt
- ✅ Interactive API documentation (Swagger UI)
- ✅ Simple and lightweight
- ✅ Easy to run locally

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## Running the API

Start the server:

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Swagger UI (Interactive docs):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Authentication

### Default Credentials

- **Username:** `admin`
- **Password:** `admin123`

### Getting an Access Token

**Option 1: Using cURL**

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Option 2: Using Swagger UI**

1. Go to http://localhost:8000/docs
2. Click on the "Authorize" button (🔒 icon at the top right)
3. Enter username: `admin` and password: `admin123`
4. Click "Authorize"
5. Now you can test all endpoints directly from the browser

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## API Endpoints

### 1. Get All Branches

**Endpoint:** `GET /api/branches`

**Headers:**
```
Authorization: Bearer {access_token}
```

**cURL Example:**

```bash
curl -X GET "http://localhost:8000/api/branches" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**Response Example:**

```json
[
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
```

## Complete Workflow Example

### Step 1: Get Access Token

```bash
# Request
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYzOTU4NzYwMH0.xyz",
  "token_type": "bearer"
}
```

### Step 2: Use Token to Access Protected Endpoint

```bash
# Request
curl -X GET "http://localhost:8000/api/branches" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYzOTU4NzYwMH0.xyz"

# Response
[
  {
    "branch_id": 1,
    "branch_code": "MATAREM",
    ...
  }
]
```

## Testing with Python

```python
import requests

# 1. Get access token
token_response = requests.post(
    "http://localhost:8000/token",
    data={
        "username": "admin",
        "password": "admin123"
    }
)
token = token_response.json()["access_token"]

# 2. Get branches
branches_response = requests.get(
    "http://localhost:8000/api/branches",
    headers={"Authorization": f"Bearer {token}"}
)
branches = branches_response.json()
print(branches)
```

## Testing with JavaScript/Fetch

```javascript
// 1. Get access token
const formData = new URLSearchParams();
formData.append('username', 'admin');
formData.append('password', 'admin123');

const tokenResponse = await fetch('http://localhost:8000/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: formData
});

const { access_token } = await tokenResponse.json();

// 2. Get branches
const branchesResponse = await fetch('http://localhost:8000/api/branches', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});

const branches = await branchesResponse.json();
console.log(branches);
```

## Error Responses

### 401 Unauthorized (No token or invalid token)

```json
{
  "detail": "Could not validate credentials"
}
```

### 401 Unauthorized (Wrong credentials)

```json
{
  "detail": "Incorrect username or password"
}
```

## Token Expiration

- Access tokens expire after **60 minutes**
- When a token expires, you'll receive a 401 error
- Simply request a new token using the `/token` endpoint

## Adding More Users

Edit the `fake_users_db` dictionary in `main.py`:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate password hash
hashed = pwd_context.hash("your_password")
print(hashed)

# Add to fake_users_db
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$...",
        "disabled": False,
    },
    "newuser": {
        "username": "newuser",
        "hashed_password": hashed,
        "disabled": False,
    }
}
```

## Adding More Branches

Edit the `branches_db` list in `main.py`:

```python
branches_db.append({
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
})
```

## Security Notes

⚠️ **Important for Production:**

1. Change the `SECRET_KEY` in `main.py` to a secure random string
2. Use environment variables for sensitive data
3. Use HTTPS in production
4. Implement rate limiting
5. Use a real database instead of in-memory data
6. Implement user registration and password reset flows
7. Add input validation and sanitization

## Why FastAPI?

FastAPI was chosen because it's:
- **Simple**: Easy to set up and run locally
- **Fast**: High performance
- **Modern**: Built-in OAuth 2.0 support
- **Well-documented**: Automatic interactive API documentation
- **Pythonic**: Clean and easy to understand code
- **Production-ready**: Can easily scale from local to production

## Troubleshooting

**Port already in use:**
```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

**Module not found:**
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt
```

**Token expired:**
Simply request a new token using the `/token` endpoint.

## License

MIT License - Feel free to use this for any purpose!
