from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from sqlalchemy import select, func

class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.collate('ru_RU.UTF-8').ilike(f'%{location}%'))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f'%{title.lower()}%'))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        return result.scalars().all()


