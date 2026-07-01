from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str
    status: str


class ProjectResponse(ProjectCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True