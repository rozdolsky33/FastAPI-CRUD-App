from typing import Optional

from app.schemas.user import (
    FullUserProfile,
    User,
)

from app.exceptions import UserNotFound

profile_infos = {
    0: {
        "short_description": "My bio short description",
        "long_bio": "My bio long description"
    }
}

users_content = {
    0: {
        "liked_posts": [1] * 9,
    }
}

class UserService:

    def __init__(self):
        pass

    async def get_all_users_with_pagination(self, start: int, limit: int) -> (list[FullUserProfile], int):
        list_of_users = []
        keys = list(profile_infos.keys())
        total = len(keys)
        for index in range(0, len(keys), 1):
            if index < start:
                continue
            current_key = keys[index]
            user = await self.get_user_info(current_key)
            list_of_users.append(user)
            if len(list_of_users) >= limit:
                break

        return list_of_users, total

    @staticmethod
    async def get_user_info(user_id: int = 0) -> FullUserProfile:
        if user_id not in profile_infos:
            raise UserNotFound(user_id=user_id)
        profile_info = profile_infos[user_id]
        user_content = users_content[user_id]

        user = User(**user_content)

        full_user_profile = {
            **profile_info,
            **user.dict()
        }

        return FullUserProfile(**full_user_profile)

    @staticmethod
    async def create_update_user(full_profile_info: FullUserProfile, user_id: Optional[int] = None) -> int:
        """
        Create user and new unique user id if not exist otherwise update the user.
        Placeholder implementation late ro be updated with DB
        :param full_profile_info: FullUserProfile - user information save in database.
        :param user_id: Optional[int] - user_id if already exist, otherwise to be set
        :return: user_id: int - existing or new user id
        """
        global profile_infos
        global users_content

        if user_id is None:
            user_id = len(profile_infos)
        liked_posts = full_profile_info.liked_posts
        short_description = full_profile_info.short_description
        long_bio = full_profile_info.long_bio

        users_content[user_id] = {"liked_posts": liked_posts,
                                  "short_description": short_description,
                                  "long_bio": long_bio

                                  }

        return user_id

    @staticmethod
    async def delete_user(user_id: int) -> None:
        global profile_infos
        global users_content
        if user_id not in profile_infos:
            raise UserNotFound(user_id=user_id)
        del profile_infos[user_id]
        del users_content[user_id]
