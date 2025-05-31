from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv
import logging
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from sqlalchemy.exc import OperationalError  # Добавлен импорт

load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение URL базы данных
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz.db")
logger.info(f"Используется DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

# Конфигурация подключения к PostgreSQL с повторными попытками
@retry(
    stop=stop_after_attempt(3),  # Максимум 3 попытки
    wait=wait_fixed(5),  # Пауза 5 секунд между попытками
    retry=retry_if_exception_type((OperationalError,)),  # Используем импортированное имя
    before_sleep=lambda retry_state: logger.warning(f"Попытка подключения {retry_state.attempt_number}/3...")
)
def create_engine_with_retry():
    if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_pre_ping=True,
            connect_args={
                "connect_timeout": 15,  # Увеличен таймаут до 15 секунд
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
        )
    else:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False}  # Только для SQLite
        )
    with engine.connect() as connection:
        logger.info("Успешное подключение к базе данных")
    return engine

engine = create_engine_with_retry()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Ошибка в сессии базы данных: {e}")
        db.rollback()
        raise
    finally:
        db.close()