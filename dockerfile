FROM zauberzeug/nicegui:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/migrations/versions && chmod -R 777 /app/data

EXPOSE 80

# Запуск миграций + приложение
CMD ["sh", "-c", "alembic upgrade head && python main.py"]