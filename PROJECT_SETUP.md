# Project Setup

## Prerequisites

Before creating a FastAPI application, make sure the following are installed:

* Python 3.10 or higher
* pip (Python package manager)

Verify installation:

```bash
python --version
pip --version
```

---

# Creating a Project

Create a new project folder:

```bash
mkdir fastapi-project
cd fastapi-project
```

---

# Creating a Virtual Environment

A virtual environment isolates project dependencies from other Python projects (like node_modules in Node).

Create virtual environment ('.venv' is just filename, u can change to 'file' too):

```bash
python -m venv .venv 
```

Activate virtual environment:

### Windows

```bash
source .venv\Scripts\activate
```

After activation, you should see:

```txt
(.venv)
```

at the beginning of your terminal.

---

# Installing Dependencies

Install FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn
```

Or install all project dependencies (create 'requirements.txt' file and write all the dependencies needed along with their version):

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the application using Uvicorn:

```bash
uvicorn main:app --reload
```

or, install

```bash
pip install "fastapi[standard]"
```

and use following command to easy run application

```bash
fastapi dev
```

---

# Accessing the Application

After starting the server:

```txt
http://localhost:8000
```

or

```txt
http://127.0.0.1:8000
```

---

# Interactive API Documentation

FastAPI automatically generates API documentation.

Swagger UI:

```txt
http://localhost:8000/docs
```

No additional configuration is required.

---

# Project Structure

A simple FastAPI project structure:

```txt
project/
│
├── .venv/
├── .env
├── requirements.txt
├── main.py
│
├── routers/
├── services/
├── models/
├── schemas/
└── utils/
```

---

# Deactivating Virtual Environment

When finished:

```bash
deactivate
```

This exits the virtual environment and returns to the system Python installation.
