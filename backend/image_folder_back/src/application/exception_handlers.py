from typing import Any, Sequence

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(PydanticToDrfErrorCoverter(exc).get_details()),
    )


class PydanticToDrfErrorCoverter:
    """
    Convert pydantic validation error format to Django Rest Framework format.
    Inspired by github.com/yezz123/pyngo
    """

    def __init__(self, original_exception: RequestValidationError):
        self.original_exception = original_exception

    def get_details(self) -> dict[str, Any]:
        drf_data: dict[str, Any] = {}
        for error in self.original_exception.errors():
            self.set_nested(drf_data, error["loc"], [error["msg"]])
        return drf_data.get('body') or drf_data

    def set_nested(self, data: dict[str, Any], keys: Sequence[str], value: Any) -> None:
        for key in keys[:-1]:
            data = data.setdefault(str(key), {})
        data[keys[-1]] = value

    def get_nested(self, data: dict[str, Any], keys: Sequence[str]) -> Any:
        for key in keys[:-1]:
            data = data[key]
        return data[keys[-1]]


def setup_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(RequestValidationError)(validation_exception_handler)
