import pytest

from helpers.functions import comparison_models


@pytest.mark.asyncio
async def test_get_me(client_with_db, create_user):
    user, accesses_token = await create_user()

    response = await client_with_db.get(
        "/users/me",
        headers={"Authorization": f"Bearer {accesses_token}"}
    )

    assert response.status_code == 200
    assert comparison_models(user, response.json())

