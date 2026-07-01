from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.user import User
from app.models.project import Project

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/")
def get_dashboard_stats(db: Session = Depends(get_db)):

    total_users = db.query(User).count()

    total_projects = db.query(Project).count()

    completed_projects = db.query(Project).filter(
        Project.status == "Completed"
    ).count()

    pending_projects = db.query(Project).filter(
        Project.status == "Pending"
    ).count()

    return {
        "total_users": total_users,
        "total_projects": total_projects,
        "completed_projects": completed_projects,
        "pending_projects": pending_projects
    }