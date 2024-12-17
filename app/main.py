"""Main file to run the FastAPI application."""

import uvicorn
from fastapi import FastAPI
from loguru import logger

from app.api.v1.routers import endpoints_trading_result

app = FastAPI()

logger.add(
    "logs/logs.json",
    format="{time} {level} {message}",
    level="INFO",
    rotation="10 MB",
    retention=10,
    compression="zip",
    serialize=True,
)

app.include_router(endpoints_trading_result.router, prefix="/api/v1")


@logger.catch
def main():
    """Start FastAPI server."""
    logger.info("FastAPI server started.")
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
