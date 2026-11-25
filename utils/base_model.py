from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    def __repr__(self):
        columns = inspect(self.__class__).c
        column_values = ", ".join([f"{column.key}={getattr(self, column.key)}" for column in columns])
        return f"{self.__class__.__name__}({column_values})"
