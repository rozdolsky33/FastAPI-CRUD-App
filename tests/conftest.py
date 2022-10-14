import pytest
from app.services.user import UserService

@pytest.fixture
def profile_infos():
    val = {
        0: {
            "short_description": "My bio short description",
            "long_bio": "My bio long description"
        }
    }
    return val

@pytest.fixture
def users_content():
    val = {
        0: {
            "liked_posts": [1] * 9,
        }
    }
    return val

@pytest.fixture
def user_service(profile_infos, users_content):
    user_service = UserService(profile_infos, users_content)
    return user_service


@pytest.fixture(scope="module")
def testing_fixture():
    print("Initialize fixture")
    return None