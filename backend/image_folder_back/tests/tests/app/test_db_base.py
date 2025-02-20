from application.db.base_class import Base


async def test_base_table_name():
    assert Base.__tablename__ == 'base'
