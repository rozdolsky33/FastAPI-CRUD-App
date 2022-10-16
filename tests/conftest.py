import pytest

from app.schemas.user import FullUserProfile


@pytest.fixture(scope="session")
def valid_user_id() -> int:
    return 0


@pytest.fixture(scope="session")
def invalid_user_delete_id() -> int:
    return 404


@pytest.fixture(scope="function")
def sample_full_user_profile() -> FullUserProfile:
    return FullUserProfile(short_description="This is short test desc",
                           long_bio="this is long bio test",
                           username="nouser14",
                           liked_posts=[1, 2, 3])
