from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from database import create_table
from model import SampleModel
from sqlmodel import select
from database import Session
from model import SampleRequest, SampleResponse, SampleUpdateRequest


app = FastAPI()


@app.on_event("startup")
def startup():
    create_table()


@app.get("/sample", response_model=list[SampleResponse], status_code=200)
async def root(session: Session):
    samples = session.exec(select(SampleModel)).all()

    # to return it as JSON response, we have to wrap it in a response_model
    # (message: str
    # sample_list: list[SampleResponse])
    return samples


@app.post("/sample", status_code=201)
async def create_sample(sample_req: SampleRequest, session: Session):
    sample = SampleModel.model_validate(sample_req)
    session.add(sample)
    session.commit()

    return JSONResponse(status_code=200, content={"message": "success"})


@app.get("/sample/{id}", response_model=SampleResponse, status_code=200)
async def get_sample(id: int, session: Session):
    sample = session.get(SampleModel, id)

    if sample is None:
        raise HTTPException(status_code=404, detail="sample not found")

    return sample


@app.delete("/sample/{id}", status_code=204)
async def delete_sample(id: int, session: Session):
    sample = session.get(SampleModel, id)

    if sample is None:
        raise HTTPException(status_code=404, detail="sample not found")

    session.delete(sample)
    session.commit()

    return JSONResponse(status_code=200, content={"message": "deleted"})


@app.put("/sample/{id}", response_model=SampleResponse, status_code=200)
async def update_sample(id: int, sample_req: SampleUpdateRequest, session: Session):
    sample = session.get(SampleModel, id)

    if sample is None:
        raise HTTPException(status_code=404, detail="sample not found")

    update_data = sample_req.model_dump(exclude_unset=True)
    sample.sqlmodel_update(update_data)

    session.add(sample)
    session.commit()
    session.refresh(sample)

    return sample
