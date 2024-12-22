"""Файл для моделей"""

from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    """Базовый класс"""

    pass


class Request(Base):
    """Клас для определения модели Request"""

    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cadastral_number: Mapped[str] = mapped_column(comment="Кадастровый номер")
    latitude: Mapped[float] = mapped_column(comment="Широта")
    longitude: Mapped[float] = mapped_column(comment="Долгота")
    score: Mapped[float] = mapped_column(nullable=True, comment="Результат запроса")
    is_completed: Mapped[bool] = mapped_column(default=False, comment="Расчет выполнен")

    def __repr__(self):
        return f"<Request {self.cadastral_number}>"
