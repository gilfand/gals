# Dockerfile
FROM zauberzeug/nicegui:latest

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Создаём нужные директории
RUN mkdir -p /app/data /app/migrations/versions && \
    chmod -R 777 /app/data /app/migrations

EXPOSE 80

# Самый стабильный способ запуска:
# 1. Миграции
# 2. Приложение
CMD ["sh", "-c", "\
    echo '========================================' && \
    echo '===     Starting Alembic Migrations    ===' && \
    echo '========================================' && \
    alembic upgrade head && \
    echo '========================================' && \
    echo '===     Migrations completed           ===' && \
    echo '===     Starting NiceGUI Application   ===' && \
    echo '========================================' && \
    python main.py \
"]