from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from typing import Optional
# from bson import ObjectId


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError('Invalid objectid')
#         return ObjectId(v)
#
#     @classmethod
#     def __get_pydantic_json_schema__(cls, core_schema, handler):
#         schema = handler(core_schema)
#         schema.update(type='string')
#         return schema


class PropertyModel(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4, alias="_id")
    property_name: str
    address: str
    city: str
    state: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {UUID: str}