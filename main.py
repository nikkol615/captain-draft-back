from fastapi import FastAPI
import uvicorn
import asyncio
from contextlib import asynccontextmanager
import logging

from database.db import global_init
import api.add_routes as api
import config.fastapi as api_config


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        logger.info("Starting Captain Draft Back application...")
        logger.info("Initializing database connection...")
        global_init()  # Initialize database connection
        logger.info("Database connection initialized successfully")
        logger.info("Captain Draft Back application started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}", exc_info=True)
        raise
    
    yield
    
    # Shutdown
    try:
        logger.info("Shutting down Captain Draft Back application...")
        logger.info("Captain Draft Back application shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}", exc_info=True)


app = FastAPI(
    title='Captain Draft Back',
    description="API для Captain Draft приложения",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add routes and middleware before app starts
try:
    api.add_routes(app)
    logger.info("Routes added successfully")
except Exception as e:
    logger.error(f"Failed to add routes: {str(e)}", exc_info=True)
    raise


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=api_config.HOST,
        port=api_config.PORT,
        reload=True,
        log_level="info"
    )