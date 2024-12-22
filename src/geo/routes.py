"""Файл с роутами"""

from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.database.database_core import SessionDep
from src.geo.orm_querys import db_request_create, db_request_update, get_db_request
from src.geo.schemes import CalcRequest
from src.geo.utils import calc_score

router = APIRouter()


@router.post("/calc/", summary="Создание запроса на расчет")
async def create_request(calc_request: CalcRequest, session: SessionDep, bg_tasks: BackgroundTasks):
    """
    Создаёт новый запрос на расчет.

    :param bg_tasks: Объект BackgroundTasks.
    :param calc_request: Объект CalcRequest, содержащий данные для расчета (кадастровый номер,
      широта и долгота).\n
    :param session: Сессия базы данных.\n
    :return: JSON-ответ с ID созданного запроса.\n
    """

    data = calc_request.dict(exclude_unset=True)

    db_request = await db_request_create(data, session)

    bg_tasks.add_task(calc_score, session, db_request.id)

    return {"id": db_request.id}


@router.get("/result/{request_id}", summary="Получение результата запроса")
async def get_result(request_id: int, session: SessionDep):
    """
    Получает результат запроса по его ID.

    :param request_id: ID запроса для получения результата.\n
    :param session: Сессия базы данных.\n
    :return: JSON-ответ с оценкой и статусом выполнения запроса.\n
    :exception: HTTPException (404): Если запрос с указанным ID не найден.\n
    """
    db_request = await get_db_request(session, request_id)

    if not db_request:
        raise HTTPException(
            status_code=404, detail=f"Request with id {request_id} not found"
        )

    return {
        "score": db_request.score,
        "status": "completed" if db_request.is_completed else "in progress",
    }
