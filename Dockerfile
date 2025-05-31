# Используем официальный образ Python 3.9-slim как базовый
FROM python:3.9-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя для безопасного запуска
RUN useradd -m -s /bin/bash appuser

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt для установки зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код приложения
COPY . .

# Меняем владельца файлов на appuser
RUN chown -R appuser:appuser /app

# Переключаемся на пользователя appuser
USER appuser

# Запускаем приложение с uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]