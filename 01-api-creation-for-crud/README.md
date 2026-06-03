# 01 - Basic CRUD API

## Overview

This project introduces the fundamentals of API development using FastAPI.

The application implements CRUD (Create, Read, Update, Delete) operations while storing data in memory using a Python list. Since no database is used, all data is lost whenever the server restarts.

---

## Learning Objectives

This project introduces:

* API creation 
* Operation on in-memory data
* Path variable
* Query parameter
* Basic success and exception response   

---

## Concepts Covered

### FastAPI Application

The application starts by creating a FastAPI instance:

```python
app = FastAPI()
```

This object acts as the entry point for registering routes and handling requests.

---

### Path Operations

Endpoints are created using decorators:

```python
@app.get("/sample")
```

```python
@app.post("/sample")
```

```python
@app.put("/sample/{id}")
```

```python
@app.delete("/sample/{id}")
```

Each decorator maps an HTTP method and URL path to a Python function.

---

## Route Declaration Order

FastAPI evaluates routes in the order they are registered.

When multiple routes can potentially match the same request, the first matching route is selected.

For this reason, fixed routes should always be declared before dynamic routes.

### Correct

```python
@app.get("/users/me")
async def get_current_user():
    pass

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    pass
```

Request:

```http
GET /users/me
```

Result:

```python
get_current_user()
```

---

### Incorrect

```python
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    pass

@app.get("/users/me")
async def get_current_user():
    pass
```

Request:

```http
GET /users/me
```

Result:

```python
user_id = "me"
```

The dynamic route matches first, preventing the fixed route from being executed.

> Note: Some frameworks such as Spring Boot automatically prioritize more specific routes. FastAPI follows a "first matching route wins" approach,  making route declaration order important when fixed and dynamic paths overlap.

---

### Path Parameters

Path parameters allow values to be passed directly through the URL.

Route:

```python
@app.get("/sample/{id}")
```

Example:

```http
GET /sample/1
```

FastAPI automatically converts the URL value into the specified Python type.

---

### Query Parameters

Query parameters are appended to the URL after `?`.

Example:

```http
PUT /sample/1?q=name=YYYY&age=20
```

Used in this project to specify extra details about the request.

Example:

```python
@app.put("/sample/{id}")
async def read_item(name: str, age: int):
    # Rest of the function
```

> `name: str` makes the query parameter required/necessary. To make it optional provide a default value for it (`name: str = None`). 

---

### Request Body Validation

FastAPI uses Pydantic models to validate incoming request data.

Example:

```python
class RequestSample(BaseModel):
    user_name: str
    age: int
```

Incoming JSON must match the defined schema.

Example:

```json
{
    "user_name": "XXXXX",
    "age": 25
}
```

If validation fails, FastAPI automatically returns an error response.

---

### In-Memory Data Storage

Data is stored in a Python list:

```python
sample_list = []
```

Although, for production level application using persistent storage like DB is encouraged.

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

FastAPI automatically converts Python objects into JSON.

Example:

```python
return {
    "message": "success"
}
```

Response:

```json
{
    "message": "success"
}
```

---

### Custom Status Codes

Responses can be customized using `JSONResponse`.

Example:

```python
return JSONResponse(
    status_code=200,
    content={
        "message": "success"
    }
)
```

Or, by defining the code (for successful execution) as argument in the path operation.

Example:

```python
@app.get(
    "/sample",
    status_code=200
)
```

---

## Error Handling

FastAPI provides `HTTPException` for returning errors.

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