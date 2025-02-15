import uvicorn

from carnival.core.config import settings
from carnival.core.logger import logger

if __name__ == "__main__":
    logger.info("\nStarting Carnival compilance Service 🎉 \n")
    uvicorn.run("carnival.app:app", host=settings.HOST, port=settings.PORT, reload=True)
