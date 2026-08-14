from typing import Tuple, List

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from helpers import comparison_models
from models.website_check.fixtures.models_dto import CreateWebsiteChecksFixtureDTO
from models.websites.fixtures.models_dto import CreateWebsiteFixtureDTO
from src.models.website_check.models import WebsiteChecks
from src.models.website_check.models_dto import WebsiteChecksDTOResponse


class TestsForSuccess:

    async def _create_website_check_user_and_other(
        self,
        user_id: int,
        website_id: int,
        create_website_check_fixture,
    ) -> Tuple[List[WebsiteChecksDTOResponse], List[WebsiteChecksDTOResponse]]:
        """
        :return: Tuple[привязанные_к_пользователю, созданы_для_другого_пользователя]
        """
        websites_check_user: List[WebsiteChecksDTOResponse] = []
        for i in range(10):
            websites_check_user.append(
                WebsiteChecksDTOResponse.model_validate(
                    await create_website_check_fixture(
                        new_websites_checks=CreateWebsiteChecksFixtureDTO(
                            user_id=user_id,
                            website_id=website_id,
                        )
                    )
                )
            )

        websites_other: List[WebsiteChecksDTOResponse] = []
        for i in range(3):
            websites_other.append(
                WebsiteChecksDTOResponse.model_validate(await create_website_check_fixture())
            )
        return websites_check_user, websites_other

    @pytest.mark.asyncio
    async def test_get_website_by_id(
        self,
        client_for_tests,
        create_user_fixture,
        create_website_check_fixture,
    ):
        user, accesses_token = await create_user_fixture()
        website_check = await create_website_check_fixture(
            new_websites_checks=CreateWebsiteChecksFixtureDTO(
                user_id=user.id,
            )
        )

        response = await client_for_tests.get(
            f"/website_check/{website_check.id}",
            headers={"Authorization": f"Bearer {accesses_token}"},
        )


        assert response.status_code == 200

        response_website_check = WebsiteChecksDTOResponse.model_validate(response.json())

        assert comparison_models(website_check, response_website_check)

    @pytest.mark.asyncio
    async def test_get_checks_by_website_id(
        self,
        client_for_tests,
        create_user_fixture,
        create_website_fixture,
        create_website_check_fixture,
    ):
        user, accesses_token = await create_user_fixture()
        website = await create_website_fixture(
            new_website=CreateWebsiteFixtureDTO(user_id=user.id)
        )
        user_checks, other_checks = await self._create_website_check_user_and_other(
            user_id=user.id,
            website_id=website.id,
            create_website_check_fixture=create_website_check_fixture,
        )

        response = await client_for_tests.get(
            f"/websites/{website.id}/checks",
            headers={"Authorization": f"Bearer {accesses_token}"},
        )

        assert response.status_code == 200

        websites_check_response = []
        for website in response.json():
            websites_check_response.append(WebsiteChecksDTOResponse.model_validate(website))

        # проверка, что вернулось
        for check in user_checks:
            assert check in websites_check_response

    @pytest.mark.asyncio
    async def test_delete_website_check(
        self,
        session_db: AsyncSession,
        client_for_tests,
        create_user_fixture,
        create_website_fixture,
        create_website_check_fixture,
    ):
        user, accesses_token = await create_user_fixture()
        website = await create_website_fixture(
            new_website=CreateWebsiteFixtureDTO(user_id=user.id)
        )
        user_checks, other_checks = await self._create_website_check_user_and_other(
            user_id=user.id,
            website_id=website.id,
            create_website_check_fixture=create_website_check_fixture,
        )

        user_check_ids = [check.id for check in user_checks]
        response = await client_for_tests.delete(
            f"/website_check",
            headers={"Authorization": f"Bearer {accesses_token}"},
            params={
                "website_checks_ids": user_check_ids
            }
        )

        assert response.status_code == 204

        # которые надо удалить
        result_db = await session_db.execute(
            select(WebsiteChecks)
            .where(
                WebsiteChecks.id.in_(user_check_ids)
            )
        )
        check_user_from_db = result_db.scalars().all()
        assert not check_user_from_db

        # которые не надо удалить
        other_check_ids = [check.id for check in other_checks]
        result_db = await session_db.execute(
            select(WebsiteChecks.id)
            .where(
                WebsiteChecks.id.in_([check.id for check in other_checks])
            )
        )
        check_other_from_db = result_db.scalars().all()
        for website_id in other_check_ids: assert website_id in check_other_from_db

    @pytest.mark.asyncio
    async def test_delete_website_checks_by_website(
            self,
            session_db: AsyncSession,
            client_for_tests,
            create_user_fixture,
            create_website_fixture,
            create_website_check_fixture,
    ):
        user, accesses_token = await create_user_fixture()
        website = await create_website_fixture(
            new_website=CreateWebsiteFixtureDTO(user_id=user.id)
        )
        user_checks, other_checks = await self._create_website_check_user_and_other(
            user_id=user.id,
            website_id=website.id,
            create_website_check_fixture=create_website_check_fixture,
        )

        user_check_ids = [check.id for check in user_checks]
        response = await client_for_tests.delete(
            f"/websites/{website.id}/checks",
            headers={"Authorization": f"Bearer {accesses_token}"},
            params={
                "website_id": user_check_ids
            }
        )

        assert response.status_code == 204

        # которые надо удалить
        result_db = await session_db.execute(
            select(WebsiteChecks)
            .where(
                WebsiteChecks.website_id == website.id,
            )
        )
        check_user_from_db = result_db.scalars().all()
        assert not check_user_from_db

        # которые не надо удалить
        other_check_ids = [check.id for check in other_checks]
        result_db = await session_db.execute(
            select(WebsiteChecks.id)
            .where(
                WebsiteChecks.id.in_([check.id for check in other_checks])
            )
        )
        check_other_from_db = result_db.scalars().all()
        for website_id in other_check_ids: assert website_id in check_other_from_db
