from fastapi import APIRouter, HTTPException

from app.schemas.user import (
    CreateUserResponse,
    FullUserProfile,
    MultipleUsersResponse
)
from app.services.user import UserService

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(levelname)-2s %(name)s %(asctime)s.%(msecs)03d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="log.txt",
)


def create_user_router() -> APIRouter:
    user_router = APIRouter(
        prefix="/users",
        tags=["Users"],
    )
    user_service = UserService()

    @user_router.get("/{user_id}", response_model=FullUserProfile)
    async def get_user_by_id(user_id: int):
        """
        Endpoint for retrieving a fullUserProfile by the users unique integer id
        :param user_id: int - unique monotonically increasing integer id
        :return: FullUserProfile
        """
        full_user_profile = await user_service.get_user_info(user_id)
        return full_user_profile

    @user_router.put("/{user_id}", status_code=204)
    async def update_user(user_id: int, full_profile_info: FullUserProfile):
        await user_service.create_update_user(full_profile_info, user_id)
        return None

    @user_router.delete("/{user_id}", status_code=204)
    async def remove_user(user_id: int):
        logger.info(f"About to delete {user_id}")
        try:
            await user_service.delete_user(user_id)
        except KeyError:
            logger.error(f"Invalid user_id {user_id}")
            raise HTTPException(status_code=404, detail={"msg": f"User doesn't exist", "user_id": user_id})

    @user_router.get("/", response_model=MultipleUsersResponse)
    async def get_all_users_paginated(start: int = 0, limit: int = 20):
        users, total = await user_service.get_all_users_with_pagination(start, limit)
        formatted_users = MultipleUsersResponse(users=users, total=total)
        return formatted_users

    @user_router.post("/", response_model=CreateUserResponse, status_code=201)
    async def add_user(full_profile_info: FullUserProfile):
        user_id = await user_service.create_update_user(full_profile_info)
        created_user = CreateUserResponse(user_id=user_id)
        return created_user

    return user_router
