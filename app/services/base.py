from sqlalchemy import delete, insert, select, update

from app.core.database import async_session_maker


class BaseService:
    model = None  # This should be set in subclasses

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add_one(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            created = result.scalar_one()
            await session.commit()
            return created

    @classmethod
    async def update_one(cls, instance, **data):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == instance.id)
                .values(**data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            updated = result.scalar_one()
            await session.commit()
            return updated

    @classmethod
    async def delete_one(cls, instance):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == instance.id)
            await session.execute(query)
            await session.commit()
            return True
