from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.models.auth.depends import get_current_user
from src.models.users.models_dto import UsersDTO
from src.models.websites.depends import get_website_service
from src.models.websites.models_dto import WebsiteResponse, CreateWebsiteDTO, CreateWebsiteRequestDTO, \
    UpdateWebsiteRequestDTO, UpdateWebsiteDTO
from src.models.websites.service import WebsitesService

router = APIRouter(prefix="/websites")


@router.post("/create_website", response_model=WebsiteResponse, status_code=status.HTTP_200_OK)
async def create_website(
    data: CreateWebsiteRequestDTO,
    user = Depends(get_current_user),
    website_service: WebsitesService = Depends(get_website_service),
):
    data_for_creating = CreateWebsiteDTO(user_id=user.id, **data.model_dump())
    result = await website_service.create_website(data_for_creating)
    return WebsiteResponse.model_validate(result)


@router.get("/get_website/{website_id}", response_model=WebsiteResponse, status_code=status.HTTP_200_OK)
async def get_website_by_id(
    website_id: int,
    user: UsersDTO = Depends(get_current_user),
    website_service: WebsitesService = Depends(get_website_service),
):
    website = await website_service.get_website(user_id=user.id, website_id=website_id)
    return WebsiteResponse.model_validate(website)


@router.get("/get_all_websites", response_model=List[WebsiteResponse], status_code=status.HTTP_200_OK)
async def get_website_by_id(
    user: UsersDTO = Depends(get_current_user),
    website_service: WebsitesService = Depends(get_website_service),
):
    websites = await website_service.get_all_websites(user_id=user.id)
    return [WebsiteResponse.model_validate(website) for website in websites]


@router.put("/update_website/{website_id}", response_model=WebsiteResponse, status_code=status.HTTP_200_OK)
async def update_website(
    website_id: int,
    data: UpdateWebsiteRequestDTO,
    user: UsersDTO = Depends(get_current_user),
    website_service: WebsitesService = Depends(get_website_service),
):
    website = await website_service.update_website(
        website_id=website_id,
        user_id=user.id,
        data=UpdateWebsiteDTO.model_validate(data)
    )
    return WebsiteResponse.model_validate(website)


@router.delete("/delete_websites", status_code=status.HTTP_204_NO_CONTENT)
async def delete_websites(
    website_ids: List[int],
    user: UsersDTO = Depends(get_current_user),
    website_service: WebsitesService = Depends(get_website_service),
):
    await website_service.delete_website(user_id=user.id, website_ids=website_ids)
    return None

