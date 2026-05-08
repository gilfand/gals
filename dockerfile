FROM zauberzeug/nicegui:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/migrations/versions && chmod -R 777 /app/data

EXPOSE 80

CMD ["sh", "-c", "echo '=== Starting migrations ===' && alembic upgrade head && echo '=== Migrations completed ===' && echo '=== Starting NiceGUI ===' && python main.py"]
