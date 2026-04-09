from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db import get_db
from app.models import UserProfile
from app.schemas.resume import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserProfileCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user profile."""
    # Check if email already exists
    result = await db.execute(select(UserProfile).where(UserProfile.email == user_data.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Create new user
    new_user = UserProfile(**user_data.model_dump())
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)

    return new_user


@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get a user profile by ID."""
    result = await db.execute(select(UserProfile).where(UserProfile.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.get("/", response_model=List[UserProfileResponse])
async def list_users(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    """List all user profiles."""
    result = await db.execute(select(UserProfile).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


@router.put("/{user_id}", response_model=UserProfileResponse)
async def update_user(
    user_id: int,
    user_data: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a user profile."""
    result = await db.execute(select(UserProfile).where(UserProfile.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Update only provided fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a user profile."""
    result = await db.execute(select(UserProfile).where(UserProfile.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    await db.delete(user)
    return None
