"""Схемы"""

from pydantic import BaseModel


class CalcRequest(BaseModel):
    """Схема для запроса"""

    cadastral_number: str
    latitude: float
    longitude: float
