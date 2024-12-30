"""Module is Repository pattern. It is used to interact with the database."""

from datetime import date
from typing import Generic, Sequence, TypeVar

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.pydantic_schemas import TradingResultBase

T = TypeVar("T", TradingResultBase, date)


class TradingResultRepository(Generic[T]):
    """Class is used to interact with the database."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute_query(self, stmt: Select) -> Sequence[T]:
        """Execute a given query and return the results."""
        result = await self.session.execute(stmt)
        return result.scalars().all()
