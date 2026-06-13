from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.models.auth.depends import get_current_user
from src.models.users.models_dto import UsersDTO
from src.models.website_check.depends import get_website_check_service
from src.models.website_check.models_dto import WebsiteChecksDTOResponse
from src.models.website_check.service import WebsiteCheckService

router = APIRouter(prefix="/website_check")


@router.get(
    "/get_website_check/{website_check_id}",
    response_model=WebsiteChecksDTOResponse,
    status_code=status.HTTP_200_OK
)
async def get_website_by_id(
    website_check_id: int,
    user: UsersDTO = Depends(get_current_user),
    website_check_service: WebsiteCheckService = Depends(get_website_check_service),
):
    website_check = await website_check_service.get_check_by_id(check_id=website_check_id, user_id=user.id)
    return WebsiteChecksDTOResponse.model_validate(website_check)


@router.get(
    "/get_checks_by_website_id/{website_id}",
    response_model=List[WebsiteChecksDTOResponse],
    status_code=status.HTTP_200_OK
)
async def get_website_by_id(
    website_id: int,
    user: UsersDTO = Depends(get_current_user),
    website_check_service: WebsiteCheckService = Depends(get_website_check_service),
):
    website_check = await website_check_service.get_checks_by_website_id(website_id=website_id, user_id=user.id)
    return [WebsiteChecksDTOResponse.model_validate(check) for check in website_check]


@router.delete("/delete_website_checks", status_code=status.HTTP_204_NO_CONTENT)
async def delete_website_checks(
    website_checks_ids: List[int],
    user: UsersDTO = Depends(get_current_user),
    website_check_service: WebsiteCheckService = Depends(get_website_check_service),
):
    await website_check_service.delete_by_ids(check_ids=website_checks_ids, user_id=user.id)
    return None


@router.delete("/delete_website_checks_by_website", status_code=status.HTTP_204_NO_CONTENT)
async def delete_website_checks_by_website(
    website_id: int,
    user: UsersDTO = Depends(get_current_user),
    website_check_service: WebsiteCheckService = Depends(get_website_check_service),
):
    await website_check_service.delete_by_website_id(website_id=website_id, user_id=user.id)
    return None