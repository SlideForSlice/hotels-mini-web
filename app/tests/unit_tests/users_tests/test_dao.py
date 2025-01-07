import pytest

from app.users.dao import UsersDAO


@pytest.mark.parametrize("user_id, email, is_present", [
    (1, "dsad", True),
    (2, "dsad", False),
    (3, "dsad", False),

])
async def test_find_user_by_id(user_id, is_present, email):
    user = await UsersDAO.find_by_id(user_id)

    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user
