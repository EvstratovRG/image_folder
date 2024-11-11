import math
from fastapi import Query
from pydantic import BaseModel
from typing import Any, List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.selectable import Select

from application import settings

PAGE_SIZE = getattr(settings, 'PAGE_SIZE', 100)
MAX_PAGE_SIZE = getattr(settings, 'MAX_PAGE_SIZE', 100)


class MetaPagination(BaseModel):
    objects_count: int
    objects_total: int
    pages_count: int
    page_number: int


class Pagination(BaseModel):
    page_size: int
    page_number: int

    @property
    def offset(self):
        return (self.page_number - 1) * self.page_size

    @property
    def limit(self):
        return self.page_size

    def get_pages_count(self, total: int) -> int:
        return math.ceil(total / self.page_size)


async def get_pagination(
        page_size: Optional[int] = Query(
            default=PAGE_SIZE,
            title='Размер страницы',
            description=f'По умолчанию: {PAGE_SIZE} (не может быть больше {MAX_PAGE_SIZE})',
            gt=0,
            le=MAX_PAGE_SIZE
        ),
        page_number: Optional[int] = Query(
            default=1,
            title='Номер страницы',
            description='По умолчанию: 1',
        )
) -> Pagination:
    return Pagination(page_size=page_size, page_number=page_number)


async def paginate_query(
        db_session: AsyncSession,
        query: Select,
        pagination: Pagination,
) -> Tuple[MetaPagination, List[Any]]:
    page_query = query.limit(pagination.limit).offset(pagination.offset)
    count_query = select(count()).select_from(query.subquery())
    page_cursor = await db_session.execute(page_query)
    count_cursor = await db_session.execute(count_query)

    total_count = count_cursor.scalar()
    items_data = list(page_cursor.fetchall())
    items_count = len(items_data)

    meta = MetaPagination(
        objects_count=items_count,
        objects_total=total_count,
        pages_count=pagination.get_pages_count(total_count),
        page_number=pagination.page_number,
    )

    return meta, items_data
