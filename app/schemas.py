from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Category = Literal["bookkeeping", "project", "research", "draft", "email", "note"]
Priority = Literal["low", "normal", "high", "urgent"]


class ItemCreate(BaseModel):
    category: Category
    title: str = Field(min_length=1, max_length=200)
    content: str = ""
    status: str = Field(default="open", max_length=30)
    priority: Priority = "normal"
    due_date: datetime | None = None
    amount: float | None = None
    details: dict = Field(default_factory=dict)


class ItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = None
    status: str | None = Field(default=None, max_length=30)
    priority: Priority | None = None
    due_date: datetime | None = None
    amount: float | None = None
    details: dict | None = None


class ItemRead(ItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class EmailTriageRequest(BaseModel):
    subject: str = Field(min_length=1, max_length=500)
    body: str = Field(default="", max_length=20000)


class EmailTriageResult(BaseModel):
    category: str
    priority: Priority
    needs_reply: bool
    summary: str
    suggested_action: str
