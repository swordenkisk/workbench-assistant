from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models import Item
from app.schemas import (
    EmailTriageRequest,
    EmailTriageResult,
    ItemCreate,
    ItemRead,
    ItemUpdate,
)
from app.services.triage import triage_email


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Workbench Assistant API",
    description=(
        "A lightweight workspace API for bookkeeping records, projects, "
        "research, drafts, notes, and email triage."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items", response_model=list[ItemRead])
def list_items(
    category: str | None = Query(default=None),
    item_status: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    statement = select(Item).order_by(Item.created_at.desc()).limit(limit)

    if category:
        statement = statement.where(Item.category == category)
    if item_status:
        statement = statement.where(Item.status == item_status)

    return list(db.scalars(statement).all())


@app.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found.")
    return item


@app.patch("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found.")

    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        if value is None and field in {"title", "content", "status", "priority", "details"}:
            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null.",
            )
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found.")

    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/triage/email", response_model=EmailTriageResult)
def email_triage(payload: EmailTriageRequest):
    return triage_email(payload.subject, payload.body)
