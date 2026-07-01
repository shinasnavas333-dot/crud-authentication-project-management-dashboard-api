from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"].lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can create projects"
        )

    new_project = Project(
        name=project.name,
        description=project.description,
        status=project.status,
        owner_id=int(current_user["sub"])
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project

@router.get("/")
def get_projects(
    search: str = "",
    status: str = "",
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db)
):

    skip = (page - 1) * limit

    query = db.query(Project)

    if search:
        query = query.filter(
            Project.name.contains(search)
        )

    if status:
        query = query.filter(
            Project.status == status
        )

    projects = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return projects2q   

@router.get("/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project

@router.put("/{project_id}")
def update_project(
    project_id: int,
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db_project.name = project.name
    db_project.description = project.description
    db_project.status = project.status

    db.commit()
    db.refresh(db_project)

    return db_project
    
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(db_project)
    db.commit()

    return {"message": "Project deleted successfully"}