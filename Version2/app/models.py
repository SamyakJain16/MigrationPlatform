from typing import Any, Annotated, Union
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from pydantic import PlainSerializer, AfterValidator, WithJsonSchema


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]


class DocumentModel(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    size: int
    date: datetime
    file_path: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class DocumentCreate(BaseModel):
    name: str
    size: int
    file_path: str
