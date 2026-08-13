from fastapi import APIRouter, HTTPException, Depends
from database import AsyncSessionDep
from schemas.user import *
from repository.user import *
from core.firebase import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
async def register(
    data: UserCreate,
    db: AsyncSessionDep,
    current_user: dict = Depends(get_current_user),
):
    # Firebase UID must match the token
    if data.id != current_user["uid"]:
        raise HTTPException(status_code=403, detail="Forbidden")

    existing = await get_user_by_id(db, data.id)
    if existing:
        return existing  # idempotent — return existing user on re-register

    return await create_user(db, data)


@router.get("/me", response_model=UserRead)
async def get_me(
    db: AsyncSessionDep,
    current_user: dict = Depends(get_current_user),
):
    user = await get_user_by_id(db, current_user["uid"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/me", response_model=UserRead)
async def update_me(
    data: UserUpdate,
    db: AsyncSessionDep,
    current_user: dict = Depends(get_current_user),
):
    user = await get_user_by_id(db, current_user["uid"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await update_display_name(db, user, data.display_name)


@router.delete("/me", status_code=204)
async def delete_me(
    db: AsyncSessionDep,
    current_user: dict = Depends(get_current_user),
):
    user = await get_user_by_id(db, current_user["uid"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await delete_user(db, user)