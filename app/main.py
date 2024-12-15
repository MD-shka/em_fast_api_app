"""Main file to run the FastAPI application."""

import uvicorn
from fastapi import FastAPI

from app.api.v1.routers import endpoints_trading_result

app = FastAPI()

app.include_router(endpoints_trading_result.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
