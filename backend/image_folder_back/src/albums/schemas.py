from pydantic import BaseModel, Field
from utils.consts import MIN_FIELD_LENGTH, MAX_FIELD_LENGTH


class CreateAlbumCategorySchema(BaseModel):
    title: str = Field(min_length=MIN_FIELD_LENGTH, max_length=MAX_FIELD_LENGTH)


class UpdateAlbumCategorySchema(CreateAlbumCategorySchema):
    pass
