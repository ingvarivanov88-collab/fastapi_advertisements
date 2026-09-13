from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models, schemas

async def create_advertisement(session: AsyncSession, data: schemas.AdvertisementCreate):
    adv = models.Advertisement(**data.dict())
    session.add(adv)
    await session.commit()
    await session.refresh(adv)
    return adv

async def get_advertisement(session: AsyncSession, adv_id: int):
    result = await session.get(models.Advertisement, adv_id)
    return result

async def update_advertisement(session: AsyncSession, adv_id: int, data: schemas.AdvertisementUpdate):
    adv = await session.get(models.Advertisement, adv_id)
    if not adv:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(adv, field, value)
    await session.commit()
    await session.refresh(adv)
    return adv

async def delete_advertisement(session: AsyncSession, adv_id: int):
    adv = await session.get(models.Advertisement, adv_id)
    if not adv:
        return None
    await session.delete(adv)
    await session.commit()
    return adv

async def search_advertisements(session: AsyncSession, title: str = None, author: str = None, min_price: float = None, max_price: float = None):
    query = select(models.Advertisement)
    if title:
        query = query.where(models.Advertisement.title.ilike(f"%{title}%"))
    if author:
        query = query.where(models.Advertisement.author.ilike(f"%{author}%"))
    if min_price is not None:
        query = query.where(models.Advertisement.price >= min_price)
    if max_price is not None:
        query = query.where(models.Advertisement.price <= max_price)
    result = await session.execute(query)
    return result.scalars().all()