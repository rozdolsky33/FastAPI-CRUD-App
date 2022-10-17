from typing import Optional, Tuple

from app.schemas.user import (
    FullUserProfile,
    User,
)

from app.exceptions import UserNotFound
from app.clients.db import DatabaseClient
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import Select


class UserService:

    def __init__(self, database_client: DatabaseClient):
        self.database_client = database_client

    async def get_all_users_with_pagination(self, offset: int, limit: int) -> Tuple[list[FullUserProfile], int]:
        query = self._get_user_info_query()
        users = self.database_client.get_paginated(query, limit, offset)

        total_query = select(func.count(self.database_client.user.c.id).label("total"))
        total = self.database_client.get_first(total_query)[0]
        user_infos = []
        for user in users:
            user_info = dict(zip(user.keys(), user))
            full_user_profile = FullUserProfile(**user_info)
            user_infos.append(full_user_profile)

        return user_infos, total

    async def get_user_info(self, users_id: int = 0) -> FullUserProfile:
        query = await self._get_user_info_query(users_id)
        users = self.database_client.get_first(query)

        if not users:
            raise UserNotFound(user_id=users_id)

        users_info = dict(zip(users.keys(), users))

        return FullUserProfile(**users_info)

    async def create_update_user(self, full_profile_info: FullUserProfile, user_id: Optional[int] = None) -> int:
        """
        Create user and new unique user id if not exist otherwise update the user.
        Placeholder implementation late ro be updated with DB
        :param full_profile_info: FullUserProfile - user information save in database.
        :param user_id: Optional[int] - user_id if already exist, otherwise to be set
        :return: user_id: int - existing or new user id
        """

        if user_id is None:
            user_id = len(self.profile_infos)
        liked_posts = full_profile_info.liked_posts
        short_description = full_profile_info.short_description
        long_bio = full_profile_info.long_bio

        self.users_content[user_id] = {"liked_posts": liked_posts}
        self.profile_infos[user_id] = {
            "short_description": short_description,
            "long_bio": long_bio
        }

        return user_id

    async def delete_user(self, user_id: int) -> None:
        if user_id not in self.profile_infos:
            raise UserNotFound(user_id=user_id)
        del self.profile_infos[user_id]
        del self.users_content[user_id]

    async def _get_user_info_query(self, users_id: Optional[int] = None) -> Select:
        liked_posts_query = (
            select(
                self.database_client.liked_post.c.users_id,
                func.array_agg(self.database_client.liked_post.c.post_id).label("liked_posts")

            )
            .group_by(self.database_client.liked_post.c.users_id)
        )
        if users_id:
            liked_posts_query = liked_posts_query.where(self.database_client.liked_post.c.users_id == users_id)
        liked_posts_query = liked_posts_query.cte("liked_posts_query")

        query = (
            select(
                self.database_client.users.c.short_description,
                self.database_client.users.c.long_bio,
                self.database_client.users.c.username.label("name"),
                liked_posts_query.c.liked_posts
            )
            .join(
                liked_posts_query,
                liked_posts_query.c.users_id == self.database_client.users.c.id,
                isouter=True
            )
        )
        if users_id:
            query = query.where(self.database_client.users.c.id == users_id)

        return query
