from fastapi.datastructures import Default
from fastapi import FastAPI
from pydantic import BaseModel
import copy
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


class RequestSample(BaseModel):
    user_name: str = Default("")
    age: int = Default(0)


class Sample:
    id: int
    user_name: str
    age: int

    def __init__(self, id: int, user_name: str, age: int):
        self.id = id
        self.user_name = user_name
        self.age = age


app = FastAPI()

sample_list = []


# Retrieve all samples stored in sample_list
@app.get("/sample")
async def get_all_sample():
    return JSONResponse(
        status_code=200,
        content={"sample_list": sample_list, "sample_size": sample_list.__len__()},
    )


# Add new sample to sample_list
@app.post("/sample")
async def add_sample(request_sample: RequestSample):
    new_sample = Sample(
        sample_list.__len__() + 1, request_sample.user_name, request_sample.age
    )

    sample_list.append(new_sample)

    return JSONResponse(
        status_code=200,
        content={"sample_position": sample_list.__len__() - 1},
    )


# Retrieve sample having id = {path variable}
@app.get("/sample/{id}")
async def get_sample(id: int):
    sample = None
    for s in sample_list:
        if s.id == id:
            sample = s
            return JSONResponse(
                status_code=200,
                content={"sample": sample},
            )

    raise HTTPException(status_code=404, detail="Sample not found")


# Delete sample having id = {path variable}
@app.delete("/sample/{id}")
async def delete_sample(id: int):
    for s in sample_list:
        if s.id == id:
            sample_list.remove(s)
            return JSONResponse(status_code=200, content={"message": "Sample deleted"})

    raise HTTPException(status_code=404, detail="Sample not found")


# Update the sample having id = {path variable} using field provided in request parameter (q)
@app.put("/sample/{id}")
async def update_sample(id: int, q: str = None):
    old_sample = [copy.deepcopy(s) for s in sample_list if s.id == id]

    change_field = [pair.split("=") for pair in q.split("&")]

    for s in sample_list:
        if s.id == id:
            for field in change_field:
                if field[0] == "user_name":
                    s.user_name = field[1]
                elif field[0] == "age":
                    s.age = int(field[1])
                else:
                    raise HTTPException(status_code=400, detail="Invalid field")

    new_sample = [copy.deepcopy(s) for s in sample_list if s.id == id]

    return JSONResponse(
        status_code=200, content={"old_sample": old_sample, "new_sample": new_sample}
    )
