# 01 - Basic CRUD API

## Overview

This project demonstrates how to create a basic CRUD (Create, Read, Update, Delete) API using FastAPI.

Data is stored in memory using a Python list, making this project suitable for learning API fundamentals before introducing databases.

After completing this project, you should understand how FastAPI handles routing, request validation, responses, status codes, and error handling.

---

## Concepts Covered

* FastAPI Application Creation
* Route Mapping
* GET Requests
* POST Requests
* PUT Requests
* DELETE Requests
* Path Parameters
* Query Parameters
* Request Body Validation
* Pydantic Models
* JSON Responses
* HTTP Status Codes
* Exception Handling using `HTTPException`
* In-Memory Data Storage (non persistant, reset on server reload)

---

## Running the Project

Follow the setup instructions in:

```txt
PROJECT_SETUP.md
```

Once the application is running, open:

```txt
http://localhost:8000/docs
```

to access Swagger UI and interact with all endpoints directly from your browser.

---

## API Endpoints

| Method | Endpoint       | Description               |
| ------ | -------------- | ------------------------- |
| GET    | `/sample`      | Retrieve all samples      |
| GET    | `/sample/{id}` | Retrieve a sample by ID   |
| POST   | `/sample`      | Create a new sample       |
| PUT    | `/sample/{id}` | Update an existing sample |
| DELETE | `/sample/{id}` | Delete a sample           |

---

## Returning Responses

FastAPI automatically converts Python objects into JSON responses.

Example:

```python
return {
    "message": "Success"
}
```

or 

Custom status codes can be returned using `JSONResponse`:

```python
return JSONResponse(
    status_code=200,
    content={
        "message": "Success"
    }
)
```

Response:

```json
{
    "message": "Success"
}
```

---

## Error Responses

FastAPI provides `HTTPException` for returning API errors.

Example:

```python
raise HTTPException(
    status_code=404,
    detail="Sample not found"
)
```

Response:

```json
{
    "detail": "Sample not found"
}
```