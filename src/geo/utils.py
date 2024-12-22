"""Файл для дополнительных функций"""

import asyncio
import random

from src.database.database_core import SessionDep
from src.geo.orm_querys import db_request_update


async def calc_score(session: SessionDep, request_id: int):
    """Эмуляция получения скор"""
    # Эмуляция долгого расчета (10-20 секунд)
    await asyncio.sleep(random.randint(10, 20))
    # Генерация случайного "скор"
    score = round(random.uniform(-100.0, 100.0), 6)

    after_data = {
        "score": score,
        "is_completed": True,
    }

    await db_request_update(after_data, session, request_id)

    return score
