# Dockerfile
# Force rebuild 2026-05-11
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
# alembic upgrade head
CMD ["python", "main.py"]