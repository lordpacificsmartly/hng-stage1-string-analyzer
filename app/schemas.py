from pydantic import BaseModel, Field, constr
from typing import Dict
from datetime import datetime


class AnalyzeRequest(BaseModel):
    value: constr(strip_whitespace=False, min_length=1)


class Properties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str = Field(min_length=64, max_length=64)
    character_frequency_map: Dict[str, int]


class StringResponse(BaseModel):
    id: str
    value: str
    properties: Properties
    created_at: datetime


class StringsListResponse(BaseModel):
    data: list[StringResponse]
    count: int
    filters_applied: dict


class NaturalLanguageResponse(BaseModel):
    data: list[StringResponse]
    count: int
    interpreted_query: dict
