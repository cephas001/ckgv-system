from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os

from core.database import get_db
from models.domain import AdminUser, AuditLog

# Initialize the router
router = APIRouter(prefix="/api/auth", tags=["Admin Authentication"])

# --- JWT CONFIGURATION ---
# Note: Ideally, move SECRET_KEY to your .env file!
SECRET_KEY = os.getenv("SECRET_KEY", "mcpherson_ckgv_secret_key_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticates an admin user and returns a secure JWT token."""
    # 1. Search for the user in the PostgreSQL Database
    result = await db.execute(select(AdminUser).where(AdminUser.Username == request.username))
    user = result.scalars().first()

    # 2. Verify user exists and password matches
    if not user or not pwd_context.verify(request.password, user.PasswordHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # 3. Write to Audit Log
    new_log = AuditLog(AdminID=user.AdminID, ActionType="ADMIN_LOGIN")
    db.add(new_log)
    await db.commit()

    # 4. Generate a secure JWT Token
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": user.Username, "role": user.Role, "exp": expiration}
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}