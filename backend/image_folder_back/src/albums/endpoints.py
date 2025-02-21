from fastapi import APIRouter, Depends, status

from albums.models import AlbumCategory
from albums.schemas import CreateAlbumCategorySchema, UpdateAlbumCategorySchema
from albums.services import CategoryService
from application.db.dependency_providers import get_session
from auth.dependencies import get_current_user
from users.models import User

router = APIRouter(prefix="/albums", tags=["albums"])


# categories
@router.get(
    "/category/{category_id}/",
    status_code=status.HTTP_200_OK,
    response_model=AlbumCategory,
)
async def get_album_category(
    category_id: int,
    service: CategoryService = Depends(
        lambda db=Depends(get_session): CategoryService(db)
    ),
) -> AlbumCategory:
    return await service.get_by_id(category_id)


@router.get(
    "/categories/", status_code=status.HTTP_200_OK, response_model=list[AlbumCategory]
)
async def get_users_categories(
    service: CategoryService = Depends(
        lambda db=Depends(get_session): CategoryService(db)
    ),
) -> list[AlbumCategory]:
    return await service.get_list()


@router.post(
    "/categories/", status_code=status.HTTP_201_CREATED, response_model=AlbumCategory
)
async def create_album_category(
    data: CreateAlbumCategorySchema,
    user: User = Depends(get_current_user),
    service: CategoryService = Depends(
        lambda db=Depends(get_session): CategoryService(db)
    ),
) -> AlbumCategory:
    return await service.create(user.id, data.model_dump())


@router.put(
    "/categories/{category_id}/",
    status_code=status.HTTP_200_OK,
    response_model=AlbumCategory,
)
async def update_album_category(
    category_id: int,
    data: UpdateAlbumCategorySchema,
    user: User = Depends(get_current_user),
    service: CategoryService = Depends(
        lambda db=Depends(get_session): CategoryService(db)
    ),
) -> AlbumCategory:
    return await service.update(category_id, user, data.model_dump())


@router.delete("/categories/{category_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_album_category(
    category_id: int,
    user: User = Depends(get_current_user),
    service: CategoryService = Depends(
        lambda db=Depends(get_session): CategoryService(db)
    ),
) -> None:
    return await service.delete(category_id)


# albums


# images


# videos
