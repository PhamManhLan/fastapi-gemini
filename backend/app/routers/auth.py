from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.security import create_access_token
from app.crud.user import authenticate_user, create_user, get_user
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.database.db import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

settings = get_settings()

@router.post("/register")
async def register(
    user_data: UserCreate,  # thay username, password riêng lẻ bằng model
    db: Session = Depends(get_db)
):
    user = get_user(db, user_data.username)
    if user:
        raise HTTPException(status_code=400, detail="Tài khoản đã tồn tại")
    
    create_user(db, user_data.username, user_data.password)
    return {"msg": "Đăng ký thành công"}

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không đúng",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}