def get_uuid_type():  # type: ignore
    from uuid import UUID

    return UUID | str


UUID_TYPE = get_uuid_type()
