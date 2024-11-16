from pydantic import BaseModel


class AuthLoginSchema(BaseModel):
    username: str
    password: str


class AuthTokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class AuthRefreshSchema(BaseModel):
    refresh_token: str
