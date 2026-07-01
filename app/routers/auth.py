from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import (UserCreate, UserLogin, UserResponse)
from app.models.user import User
from app.dependencies.db import get_db
from app.services.auth import (
    hash_password,
    verify_password
)
from app.services.jwt import create_access_token
from app.services.jwt import verify_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme)
):
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),

    role=user.role
    )

    db.add(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "uuid": new_user.uuid,
        "username": new_user.username,
        "email": new_user.email,
        "message": "User Registered Successfully"
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm =
Depends(),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    for u in users:
        print("EMAIL:",u.email,"ROLE",u.role)

    db_user = db.query(User).filter(
        User.uuid == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    print("stored password:",db_user.hashed_password)
    print("length:", len(db_user.hashed_password))

    if not verify_password(
        form_data.password,
        db_user.hashed_password
        ):

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
    data={
        "sub": str(db_user.id),
        "email": db_user.email,
        "role": db_user.role
    }
)

    return { 
    "access_token": access_token,
    "token_type": "bearer",
    "role": db_user.role
}


@router.get("/me")
def me(token: str =
Depends(oauth2_scheme)):
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    return payload