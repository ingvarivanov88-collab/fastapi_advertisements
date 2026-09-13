from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from . import schemas, crud
from .database import engine, Base, get_session

app = FastAPI(title="Advertisement API")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/advertisement", response_model=schemas.AdvertisementRead, status_code=201)
async def create_advertisement(data: schemas.AdvertisementCreate, session: AsyncSession = Depends(get_session)):
    return await crud.create_advertisement(session, data)

@app.get("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementRead)
async def get_advertisement(advertisement_id: int, session: AsyncSession = Depends(get_session)):
    adv = await crud.get_advertisement(session, advertisement_id)
    if not adv:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return adv

@app.patch("/advertisement/{advertisement_id}", response_model=schemas.AdvertisementRead)
async def update_advertisement(advertisement_id: int, data: schemas.AdvertisementUpdate, session: AsyncSession = Depends(get_session)):
    adv = await crud.update_advertisement(session, advertisement_id, data)
    if not adv:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return adv

@app.delete("/advertisement/{advertisement_id}")
async def delete_advertisement(advertisement_id: int, session: AsyncSession = Depends(get_session)):
    adv = await crud.delete_advertisement(session, advertisement_id)
    if not adv:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return {"message": "Advertisement deleted"}

@app.get("/advertisement", response_model=List[schemas.AdvertisementRead])
async def search_advertisements(
    title: Optional[str] = None,
    author: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    session: AsyncSession = Depends(get_session),
):
    return await crud.search_advertisements(session, title, author, min_price, max_price)