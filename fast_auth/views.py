from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from fast_auth.models import User
from fast_auth.schemas import UserPublic, UserSchema, UserList
from fast_auth.database import get_session


router = APIRouter(prefix="/auth", tags=["Auth"])


Session = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=UserList)
async def list_users(session: Session):
    query = await session.scalars(
        select(User)
    )
    
    users = query.all()
    return {"users": users}


@router.post("", status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: Session):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username))
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )

    db_user = User(
        username=user.username,
        password=user.password,
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user

@router.delete("", status_code=HTTPStatus.OK, response_model=dict)
async def delete_user(user_id: int, session: Session):
    print("Deleting user with ID:", user_id)
    db_user = await session.scalar(
        select(User).where(
            (User.id == user_id))
    )
    print("Found user:", db_user)
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    await session.delete(db_user)
    await session.commit()

    return {}