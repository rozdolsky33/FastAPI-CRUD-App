import pytest

from app.services.user import UserService


@pytest.mark.asyncio
async def test_delete_works_properly(profile_infos, users_content, user_service):
    user_to_delete = 0
    await user_service.delete_user(user_to_delete)
    assert user_to_delete not in profile_infos
    assert user_to_delete not in users_content
