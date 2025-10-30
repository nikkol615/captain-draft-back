import logging

import sqlalchemy as sa
from sqlalchemy import orm as orm
from sqlalchemy.orm import Session
import inspect
from sqlalchemy.ext import declarative as dec

from config.database import DB_LINK

SqlAlchemyBase = dec.declarative_base()

log = logging.getLogger(__name__)


def _create_session() -> Session:
    """
    Создает новую сессию

    Returns:
        Session: Сессия
    """
    global __factory
    if not __factory:
        raise RuntimeError("Database not initialized. Call global_init() first.")
    return __factory()


def create_session(func):
    """
    Пропускает новую сессию как db kwarg

    Args:
        func: Функция
    Returns:
        Any: Результат функции
    """
    argspec = inspect.getfullargspec(func)

    async def wrapper(*args, **kwargs):
        """
        Обертка для создания сессии

        Args:
            *args: Аргументы
            **kwargs: Ключевые аргументы
        Returns:
            Any: Результат функции
        """
        try:
            with _create_session() as session:
                if argspec.varkw is None:
                    kwargs = {
                        k: v
                        for k, v in kwargs.items()
                        if k in argspec.args or k in argspec.kwonlyargs
                    }
                return await func(*args, **kwargs, db=session)
        except Exception as e:
            log.error(f"Error in create_session wrapper: {str(e)}", exc_info=True)
            raise

    return wrapper


__factory = None


def global_init():
    """
    Инициализирует базу данных

    Returns:
        None
    """
    global __factory

    if __factory:
        log.info("Database already initialized")
        return

    try:
        log.info(f"Connecting to PostgreSQL database: {DB_LINK}")
        
        engine = sa.create_engine(DB_LINK, echo=False)
        __factory = orm.sessionmaker(bind=engine)
        
        log.info("Creating database tables...")
        SqlAlchemyBase.metadata.create_all(engine)
        log.info("Database tables created successfully")
        
    except Exception as e:
        log.error(f"Failed to initialize PostgreSQL database: {str(e)}", exc_info=True)
        raise