"""Main file to run the FastAPI application."""

import uvicorn
from fastapi import FastAPI

from app.api.v1.routers import last_trading_dates

app = FastAPI()

app.include_router(last_trading_dates.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
