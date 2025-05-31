from celery import Celery
from dotenv import load_dotenv
from transliterate import translit
from app.logging_config import logger
import os

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    raise ValueError("REDIS_URL is not set in .env file")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
    broker_connection_retry_on_startup=True  # Добавляем настройку для устранения предупреждения
)

@celery.task
def generate_email_for_employee(full_name: str):
    logger.info(f"Генерация почты для: {full_name}")

    name_parts = full_name.split()
    if len(name_parts) >= 2:
        first_initial = translit(name_parts[1][0], 'ru', reversed=True).upper()
        last_name = translit(name_parts[0], 'ru', reversed=True).lower()
        mail_generate = f"{first_initial}.{last_name}"
    else:
        mail_generate = translit(full_name, 'ru', reversed=True).lower()

    email = f"{mail_generate}@cyber-ed.ru"
    logger.info(f"Удачная генерация почты: {email}")
    return email