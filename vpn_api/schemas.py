import uuid
from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field
from sqlalchemy import UUID, TIMESTAMP


class Users(BaseModel):
    user_wallet: str = Field(min_length=15)


class Users_id(BaseModel):
    user_id: str


class UserConfigData(BaseModel):
    user_id: uuid.UUID
    server_id: int


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    user_id: str
    user_wallet: str
    user_plan: str
    user_status: str
    user_create_date: str


class UserOut(BaseModel):
    user_id: uuid.UUID
    user_wallet: str = Field(min_length=15)
    user_plan: Union[uuid.UUID, None] = None
    user_status: bool
    user_create_date: datetime


class PlansModelOut(BaseModel):
    id: Union[uuid.UUID, None] = None
    user_id: Union[uuid.UUID, None] = None
    user_plan: Union[int, None] = None
    user_plan_status: Union[bool, None] = None
    user_plan_start: Union[datetime, None] = None
    user_plan_end: Union[datetime, None] = None


class PlansModelIn(BaseModel):
    user_id: uuid.UUID
    user_plan: int
