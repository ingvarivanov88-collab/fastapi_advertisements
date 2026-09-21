from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from . import schemas, crud
from .database import engine, Base, get_session

app = FastAPI(title="Advertisement API")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# --- ОБЪЯВЛЕНИЯ ---
@app.post("/advertisement", response_model=schemas.AdvertisementRead, status_code=201)
async def create_advertisement(
    data: schemas.AdvertisementCreate,
    session: AsyncSession = Depends(get_session),
):
    # В части 1 без авторизации: автор передаётся явно (author_id = 1 по умолчанию)
    return await crud.create_advertisement(session, data, author_id=1)


@app.get("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementRead)
async def get_advertisement(advertisement_id: int, session: AsyncSession = Depends(get_session)):
    adv = await crud.get_advertisement(session, advertisement_id)
    if not adv:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return adv


@app.patch("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementRead)
async def update_advertisement(
    advertisement_id: int,
    data: schemas.AdvertisementUpdate,
    session: AsyncSession = Depends(get_session),
):
    adv = await crud.update_advertisement(session, advertisement_id, data)
    if not adv:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return adv


@app.delete("/advertisement/{advertisement_id}")
async def delete_advertisement(
    advertisement_id: int,
    session: AsyncSession = Depends(get_session),
):
    adv = await crud.delete_advertisement(session, advertisement_id)
    if not adv:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return {"message": "Advertisement deleted"}


@app.get("/advertisement", response_model=List[schemas.AdvertisementRead])
async def search_advertisements(
    title: Optional[str] = None,
    description: Optional[str] = None,
    author_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    created_from: Optional[datetime] = None,
    created_to: Optional[datetime] = None,
    session: AsyncSession = Depends(get_session),
):
    return await crud.search_advertisements(
        session,
        title=title,
        description=description,
        author_id=author_id,
        min_price=min_price,
        max_price=max_price,
        created_from=created_from,
        created_to=created_to,
    )