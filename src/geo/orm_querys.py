"""Файл для функций работающих с БД"""

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.geo.models import Request


async def db_request_create(data, session):
    """
    Создаёт новую запись в таблице запросов.

    :param data: Словарь с данными для создания запроса.
    :param session: Сессия базы данных.
    :return: Созданный объект Request.
    :exception: HTTPException (500): Ошибка при создании записи в базе данных.
    """
    try:
        req = Request()
        for key, value in data.items():
            if hasattr(req, key):
                setattr(req, key, value)

        session.add(req)
        await session.commit()
        await session.refresh(req)

        return req
    except SQLAlchemyError as ex:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка при создании записи: {str(ex)}"
        ) from ex


async def get_db_request(session, request_id):
    """
    Возвращает запись из таблицы запросов по её ID.

    :param session: Сессия базы данных.
    :param request_id: ID запроса для получения.
    :return: Объект Request или None, если запись не найдена.
    :exception: HTTPException (500): Ошибка при получении записи из базы данных.
    """

    try:
        query = select(Request).filter(Request.id == request_id)
        result = await session.execute(query)
        return result.scalars().first()
    except SQLAlchemyError as ex:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при получении записи: {str(ex)}"
        ) from ex


async def db_request_update(data, session, request_id):
    """
    Обновляет существующую запись в таблице запросов.

    :param data: Словарь с данными для обновления запроса.
    :param session: Сессия базы данных.
    :param request_id: ID запроса для обновления.
    :return: Обновлённый объект Request.
    :exception: HTTPException (404): Если запрос с указанным ID не найден.
    :exception: HTTPException (500): Ошибка при обновлении записи в базе данных.
    """

    db_request = await get_db_request(session, request_id)

    if not db_request:
        raise HTTPException(
            status_code=404, detail=f"Request with id {request_id} not found"
        )

    try:
        if db_request:
            for key, value in data.items():
                if hasattr(db_request, key):
                    setattr(db_request, key, value)

        await session.commit()
        await session.refresh(db_request)

        return db_request
    except SQLAlchemyError as ex:
        await session.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка при обновлении записи: {str(ex)}"
        ) from ex
