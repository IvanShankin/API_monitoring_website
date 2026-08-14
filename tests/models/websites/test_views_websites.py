from typing import List, Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from helpers import comparison_models
from models.websites.fixtures.models_dto import CreateWebsiteFixtureDTO
from src.models.websites.models import Websites
from src.models.websites.models_dto import WebsiteResponse, CreateWebsiteRequestDTO, UpdateWebsiteRequestDTO


class TestsForSuccess:

    async def _create_website_user_and_other(
        self,
        user_id: int,
        create_website_fixture
    ) -> Tuple[List[WebsiteResponse], List[WebsiteResponse]]:
        """
        :return: Tuple[привязанные_к_пользователю, созданы_для_другого_пользователя]
        """
        websites_user: List[WebsiteResponse] = []
        for i in range(10):
            websites_user.append(
                WebsiteResponse.model_validate(
                    await create_website_fixture(
                        new_website=CreateWebsiteFixtureDTO(user_id=user_id)
                    )
                )
            )

        websites_other: List[WebsiteResponse] = []
        for i in range(3):
            websites_other.append(
                WebsiteResponse.model_validate(await create_website_fixture())
            )
        return websites_user, websites_other

    @pytest.mark.asyncio
    async def test_create_website(
        self,
        client_for_tests,
        create_user_fixture,
        session_db: AsyncSession
    ):
        user, accesses_token = await create_user_fixture()

        response = await client_for_tests.post(
            "/websites",
            headers={"Authorization": f"Bearer {accesses_token}"},
            json=CreateWebsiteRequestDTO(
                url="test url",
                name = "test website",
            ).model_dump(),
        )

        assert response.status_code == 200
        new_website = WebsiteResponse.model_validate(response.json())

        result_db = await session_db.execute(select(Websites).where(Websites.id == new_website.id))
        website_from_db = result_db.scalar_one_or_none()

        assert comparison_models(new_website, website_from_db)

    @pytest.mark.asyncio
    async def test_get_website_by_id(
        self,
        client_for_tests,
        session_db: AsyncSession,
        create_user_fixture,
        create_website_fixture
    ):
        user, accesses_token = await create_user_fixture()
        website = await create_website_fixture(
            new_website=CreateWebsiteFixtureDTO(
                user_id=user.id,
            )
        )

        response = await client_for_tests.get(
            f"/websites/{website.id}",
            headers={"Authorization": f"Bearer {accesses_token}"},
        )

        assert response.status_code == 200

        response_website = WebsiteResponse.model_validate(response.json())

        assert comparison_models(website, response_website)


    @pytest.mark.asyncio
    async def test_get_all_websites(
        self,
        client_for_tests,
        session_db: AsyncSession,
        create_user_fixture,
        create_website_fixture
    ):
        user, accesses_token = await create_user_fixture()

        websites_user, websites_other = await self._create_website_user_and_other(
            user.id,
            create_website_fixture,
        )

        response = await client_for_tests.get(
            f"/websites",
            headers={"Authorization": f"Bearer {accesses_token}"},
        )

        assert response.status_code == 200

        websites_response = []
        for website in response.json():
            websites_response.append(WebsiteResponse.model_validate(website))

        # проверка, что вернулось
        for website_user in websites_user:
            assert website_user in websites_response

        for website_other in websites_other:
            assert not website_other in websites_response


    @pytest.mark.asyncio
    async def test_update_website(
        self,
        client_for_tests,
        session_db: AsyncSession,
        create_user_fixture,
        create_website_fixture
    ):
        user, accesses_token = await create_user_fixture()
        website = await create_website_fixture(
            new_website=CreateWebsiteFixtureDTO(
                user_id=user.id,
            )
        )

        response = await client_for_tests.put(
            f"/websites/{website.id}",
            headers={"Authorization": f"Bearer {accesses_token}"},
            json=UpdateWebsiteRequestDTO(
                    name="new_name",
                    description="new_description",
                    check_interval_seconds=100,
                    timeout_in_seconds=17,
                    is_active=False,
            ).model_dump()
        )

        assert response.status_code == 200
        updated_website = WebsiteResponse.model_validate(response.json())

        assert updated_website.name == "new_name"
        assert updated_website.timeout_in_seconds == 17

        result_db = await session_db.execute(select(Websites).where(Websites.id == website.id))
        website_from_db = result_db.scalar_one_or_none()

        assert website_from_db.name == "new_name"
        assert website_from_db.timeout_in_seconds == 17

        assert comparison_models(updated_website, website_from_db)

    @pytest.mark.asyncio
    async def test_delete_website(
        self,
        client_for_tests,
        session_db: AsyncSession,
        create_user_fixture,
        create_website_fixture
    ):
        user, accesses_token = await create_user_fixture()

        websites_user, websites_other = await self._create_website_user_and_other(
            user.id,
            create_website_fixture,
        )

        response = await client_for_tests.delete(
            f"/websites",
            headers={"Authorization": f"Bearer {accesses_token}"},
            params=[
                ("website_ids", website.id)
                for website in websites_user
            ]
        )

        assert response.status_code == 204

        # которые надо удалить
        result_db = await session_db.execute(
            select(Websites)
            .where(
                Websites.id.in_([website.id for website in websites_user])
            )
        )
        websites_user_from_db = result_db.scalars().all()
        assert not websites_user_from_db

        # которые не надо удалить
        other_website_ids = [website.id for website in websites_other]
        result_db = await session_db.execute(
            select(Websites.id)
            .where(
                Websites.id.in_(other_website_ids)
            )
        )
        websites_other_from_db = result_db.scalars().all()
        for website_id in other_website_ids: assert website_id in websites_other_from_db


