# 02 - CRUD API with SQLite and SQLModel

## Overview

This project builds upon the previous in-memory CRUD API by introducing persistent storage using SQLite and SQLModel.

Instead of storing data in Python lists, records are now stored in a database. This allows data to persist across application restarts and introduces concepts commonly used in real-world backend applications.

---

## Concepts Covered

### Database Integration

This project introduces:

* SQLite Database
* SQLModel ORM
* Database Engine
* Database Sessions
* Table Creation
* Dependency Injection
* CRUD Operations using SQLModel

---

### Request and Response Models

The project separates database models from API models.

#### Database Model

Represents the actual database table.

```python
class SampleModel(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    name: str
    description: str
```

---

#### Request Models

Used to validate incoming requests.

```python
class SampleRequest(SQLModel):
    name: str
    description: str
```

Benefits:

* Input validation
* Separation of concerns
* Prevents clients from modifying server-controlled fields (i.e. id, creation date, etc.)

---

#### Response Models

Used to control data returned to clients.

```python
class SampleResponse(SampleBase):
    id: int
    name: str
```

Benefits:

* Hides internal fields
* Controls API contract
* Prevents accidental data exposure

---

## Database Setup

### Engine

```python
engine = create_engine(
    {db_url},
    connect_args={
        "check_same_thread": False # share db connection across multiple threads
    }
)
```

The engine acts as the connection between FastAPI and the database.

```text
FastAPI
    ↓
Engine
    ↓
SQLite
```

---

### Table Creation

```python
SQLModel.metadata.create_all(engine)
```

Creates all registered SQLModel tables if they do not already exist (i.e. all models created using keyword **SQLModel**).

Executed during application startup:

```python
@app.on_event("startup")
def startup():
    create_table()
```

---

### Database Sessions

```python
def get_session():
    with Session(engine) as session:
        yield session
```

A session is responsible for executing queries and managing data in DB

---

### Dependency Injection

```python
SessionDep = Annotated[
    Session,
    Depends(get_session)
]
```

FastAPI automatically creates and closes database sessions for each request.

Usage:

```python
async def get_samples(
    session: SessionDep
):
    ...
```

---

## API Endpoints

| Method | Endpoint       | Description           |
| ------ | -------------- | --------------------- |
| GET    | `/sample`      | Retrieve all samples  |
| GET    | `/sample/{id}` | Retrieve sample by ID |
| POST   | `/sample`      | Create a sample       |
| PUT    | `/sample/{id}` | Update a sample       |
| DELETE | `/sample/{id}` | Delete a sample       |

---

## SQLModel CRUD Operations

### Create

```python
session.add(sample)
session.commit()
session.refresh(sample)
```

Flow:

```text
Create Object
      ↓
Add To Session
      ↓
Commit Transaction
      ↓
Refresh Generated Values (only if server has to return the newly saved DB record)
```

---

### Read

Single record:

```python
session.get(
    SampleModel,
    id
)
```

Multiple records:

```python
session.exec(
    select(SampleModel)
).all()
```

---

### Update

```python
sample.name = sample_req.name

session.add(sample)
session.commit()
```

Updates an existing record and persists changes.

---

## Partial Updates

The project supports partial updates by using an update-specific request model.

Example:

```python
class SampleUpdateRequest(SQLModel):
    name: str | None = None
    description: str | None = None
```

Unlike create requests, all fields are optional.

This allows clients to update only the fields they want to modify.

Example request:

```json
{
    "name": "Updated Sample"
}
```

The client does not need to resend every field of the resource.

---

### Extracting Updated Fields

```python
update_data = sample_req.model_dump(
    exclude_unset=True
)
```

`exclude_unset=True` ensures that only fields explicitly provided by the client are included.

Example:

Request:

```json
{
    "name": "Updated Sample"
}
```

Result:

```python
{
    "name": "Updated Sample"
}
```

Without `exclude_unset=True`, fields not sent by the client would be included as `None`, potentially overwriting existing data.

---

### Updating the Database Entity

```python
sample.sqlmodel_update(update_data)
```

`sqlmodel_update()` automatically updates the model using values from the provided dictionary.

Equivalent manual implementation:

```python
for key, value in update_data.items():
    setattr(sample, key, value)
```

Using `sqlmodel_update()` is cleaner and is the recommended SQLModel approach.

---

### Update Flow

```text
Client Request
       ↓
Update Request Model
       ↓
model_dump(exclude_unset=True)
       ↓
sqlmodel_update()
       ↓
session.commit()
       ↓
Updated Database Record
```

---

### Why This Is Useful

Suppose the database contains:

```json
{
    "id": 1,
    "name": "FastAPI",
    "description": "Learning SQLModel"
}
```

Client request:

```json
{
    "name": "FastAPI Advanced"
}
```

After update:

```json
{
    "id": 1,
    "name": "FastAPI Advanced",
    "description": "Learning SQLModel"
}
```

Notice that `description` remains unchanged because it was not included in the request.

This pattern is commonly used in production APIs and is especially useful for PATCH-style updates.

---

### Delete

```python
session.delete(sample)
session.commit()
```

Removes the record from the database.

---

## Response Handling

### Automatic JSON Serialization

FastAPI automatically converts Python objects into JSON.

Example:

```python
return sample
```

No explicit JSON conversion is required.

---

### Response Models

Example:

```python
@app.get(
    "/sample",
    response_model=list[SampleResponse]
)
```

FastAPI will:

* Validate the response
* Serialize objects into JSON
* Filter fields not present in the response model

---

## Response Wrapper Pattern

Sometimes APIs return additional metadata alongside data.

Example:

```json
{
    "message": "success",
    "sample_list": [...]
}
```

To support this structure, create a wrapper model:

```python
class SampleListResponse(SQLModel):
    message: str
    sample_list: list[SampleResponse]
```

Then:

```python
@app.get(
    "/sample",
    response_model=SampleListResponse
)
```

This ensures the response matches the declared schema.

---

## Error Handling

The project uses FastAPI's HTTPException.

Example:

```python
raise HTTPException(
    status_code=404,
    detail="sample not found"
)
```

Response:

```json
{
    "detail": "sample not found"
}
```

---

## Why Separate Models?

The project demonstrates a common production pattern:

```text
Database Model
        ↓
Request Models
        ↓
Response Models
```

This allows:

* Validation
* Encapsulation
* Security
* Better API contracts

and prevents exposing database entities directly to clients.
