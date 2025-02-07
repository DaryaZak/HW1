
from typing import Annotated, Optional
from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import async_session

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[Optional[int] | None, Query(1, ge=1)]
    per_page: Annotated[Optional[int] | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams,Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401,detail="Вы не предоставили токен доступа")
    return token

def get_currant_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]

def get_user_id_dep(user_id: int = Depends(get_currant_user_id)) -> int:
    return user_id



UserIdDep = Annotated[int, Depends(get_currant_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]