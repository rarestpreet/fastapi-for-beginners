from typing import Optional
from sqlmodel import SQLModel, Field


class SampleBase(SQLModel):
    name: str


class SampleModel(SampleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str


class SampleRequest(SampleBase):
    description: str


class SampleResponse(SampleBase):
    id: int


class SampleUpdateRequest(SampleBase):
    description: str | None = None
    name: str | None = None
