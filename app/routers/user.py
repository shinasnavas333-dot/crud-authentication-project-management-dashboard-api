from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users(
    db: Session = Depends(get_db),
   current_user: dict = Depends(get_current_user)
):

    if current_user["role"].lower() != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can view users"
        )

    users = db.query(User).all()
    return users

@router.put("//{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = hash_password(user.password)

    db.commit()
    db.refresh(db_user)

    return db_user

@router.delete("/{user_id}" )
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict =
Depends(get_current_user)
):
    if current_user["role"].lower() !="admin":raise HTTPException(
            status_code=403,
            detail="Only admin can delete users"
        )
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(db_user)
    db.commit()

    return {"message": "User deleted successfully"}