# FastAPI

## What is FastAPI?

FastAPI is a modern, high-performance Python web framework used for building APIs. It is easy to learn, supports asynchronous programming, provides automatic request validation, and generates API documentation automatically.

---

# Most Common Dependencies Required to Create a FastAPI Application

## 1. FastAPI

### Purpose

FastAPI is the core framework responsible for:

* Route handling
* Request validation
* Response serialization
* Dependency Injection
* Automatic Swagger/OpenAPI documentation

### Installation

```bash
pip install fastapi
```

### Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
```

---

## 2. Uvicorn

### Purpose

Uvicorn is an ASGI server that runs FastAPI applications and handles incoming HTTP requests.

It is similar to Tomcat in Spring Boot applications.

### Installation

```bash
pip install uvicorn
```

### Running the Application

```bash
uvicorn main:app --reload
```

---

## 3. Pydantic

### Purpose

Pydantic validates request data and ensures it follows rules defined by the server.

### Installation

```bash
pip install pydantic
```

### Example

```python
from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    age: int
```

FastAPI automatically validates incoming JSON against this schema.

---

## 4. Python-Dotenv

### Purpose

Python-Dotenv loads environment variables from a `.env` file.

It is commonly used for:

* Database URLs
* JWT Secrets
* API Keys
* Application Configuration

### Installation

```bash
pip install python-dotenv
```

### Example

`.env`

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
JWT_SECRET=my-secret-key
```

Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
```

---

## 5. SQLAlchemy

### Purpose

SQLAlchemy is the most popular ORM (Object Relational Mapper) for Python.

It allows developers to work with Python objects instead of writing raw SQL queries everywhere.

### Installation

```bash
pip install sqlalchemy
```

### Example

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
```

---

## 6. Passlib + Bcrypt

### Purpose

Used for securely hashing passwords before storing them in the database.

Never store plain text passwords.

### Installation

```bash
pip install passlib bcrypt
```

### Example

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

hashed_password = pwd_context.hash("password123")
```

Verify Password:

```python
pwd_context.verify(
    "password123",
    hashed_password
)
```

---

## 7. PyJWT

### Purpose

Used for creating and validating JWT tokens.

JWTs are commonly used for authentication and authorization.

### Installation

```bash
pip install pyjwt
```

### Example

```python
import jwt

token = jwt.encode(
    {"user_id": 1},
    "secret",
    algorithm="HS256"
)
```

Decode:

```python
payload = jwt.decode(
    token,
    "secret",
    algorithms=["HS256"]
)
```

---

## 8. Python Multipart

### Purpose

Required for handling file uploads and form data.

Without this dependency, FastAPI cannot process multipart/form-data requests.

### Installation

```bash
pip install python-multipart
```

### Example

```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    return {
        "filename": file.filename
    }
```

---

## 9. HTTPX

### Purpose

HTTPX is an HTTP client used to call external APIs from FastAPI applications.

Examples:

* OpenAI API
* Gemini API
* Payment APIs
* Other Microservices

### Installation

```bash
pip install httpx
```

### Example

```python
import httpx

response = httpx.get(
    "https://api.github.com"
)

print(response.json())
```

---

# Typical Requirements File

```txt
fastapi
uvicorn[standard]
pydantic
python-dotenv
sqlalchemy
psycopg2-binary
passlib[bcrypt]
pyjwt
python-multipart
httpx
```

These dependencies are sufficient for most beginner and intermediate FastAPI projects involving authentication, databases, file uploads, and external API integrations.
