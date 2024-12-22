"""Файл для дополнительных функций"""

import asyncio
import random


async def calc_score():
    """Эмуляция получения скор"""
    # Эмуляция долгого расчета (10-20 секунд)
    await asyncio.sleep(random.randint(10, 20))
    # Генерация случайного "скор"
    score = round(random.uniform(-100.0, 100.0), 6)

    return score
