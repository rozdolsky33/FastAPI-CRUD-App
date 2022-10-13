from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class User(BaseModel):
    username: str = Field(
        alias="name",
        title="The Username",
        description="This is the username of the user",
        min_length=1,
        default=None
    )
    liked_posts: list[int] = Field(
        description="Array of post ids the user liked",
    )


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


class FullUserProfile(User):
    short_description: str
    long_bio: str


class CreateUserResponse(BaseModel):
    user_id: int


class MultipleUsersResponse(BaseModel):
    users: list[FullUserProfile]
    total: int


def get_user_info(user_id: int = 0) -> FullUserProfile:
    profile_info = profile_infos[user_id]

    user_content = users_content[user_id]
    user = User(**user_content)

    full_user_profile = {
        **profile_info,
        **user.dict()
    }

    return FullUserProfile(**full_user_profile)


def create_update_user(full_profile_info: FullUserProfile, new_user_id: Optional[int] = None) -> int:
    global profile_infos
    global users_content

    if new_user_id is None:
        new_user_id = len(profile_infos)
    liked_posts = full_profile_info.liked_posts
    short_description = full_profile_info.short_description
    long_bio = full_profile_info.long_bio

    users_content[new_user_id] = {"liked_posts": liked_posts,
                                  "short_description": short_description,
                                  "long_bio": long_bio

                                  }

    return new_user_id


def get_all_users_with_pagination(start: int, limit: int) -> (list[FullUserProfile], int):
    list_of_users = []
    keys = list(profile_infos.keys())
    total = len(keys)
    for index in range(0, len(keys), 1):
        if index < start:
            continue
        current_key = keys[index]
        user = get_user_info(current_key)
        list_of_users.append(user)
        if len(list_of_users) >= limit:
            break

    return list_of_users, total


def delete_user(user_id: int) -> None:
    global profile_infos
    global users_content

    del profile_infos[user_id]
    del users_content[user_id]


@app.get("/user/me", response_model=FullUserProfile)
def test_endpoint():
    return get_user_info()


@app.get("/user/{user_id}", response_model=FullUserProfile)
def get_user_by_id(user_id: int):
    full_user_profile = get_user_info(user_id)
    return full_user_profile


@app.put("/users/{user_id}")
def update_user(user_id: int, full_profile_info: FullUserProfile):
    create_update_user(full_profile_info, user_id)
    return None


@app.delete("/users/{user_id}")
def remove_user(user_id: int):
    delete_user(user_id)


@app.get("/users", response_model=MultipleUsersResponse)
def get_all_users_paginated(start: int = 0, limit: int = 20):
    users, total = get_all_users_with_pagination(start, limit)
    formatted_users = MultipleUsersResponse(users=users, total=total)
    return formatted_users


@app.post("/users", response_model=CreateUserResponse)
def add_user(full_profile_info: FullUserProfile):
    user_id = create_update_user(full_profile_info)
    created_user = CreateUserResponse(user_id=user_id)
    return created_user
