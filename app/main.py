from fastapi import FastAPI
from app.database import engine, Base
from app.models.user import User
from app.routers.auth import router as auth_router
from app.routers.project import router as project_router
from app.routers.user import router as user_router
from app.routers.dashboard import router as dashboard_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="project Management API",
    description="JWT Authentication, User Management and Project management System",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(project_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "Auth CRUD API Running"}