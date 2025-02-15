import uvicorn

from carnival.core.logger import logger

if __name__ == "__main__":
    # TODO:: Load from .env and scale workers
    logger.info("\nStarting Carnival compilance Service 🎉 \n")
    uvicorn.run("carnival.app:app", host="0.0.0.0", port=7000, reload=True)
