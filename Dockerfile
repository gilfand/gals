# Dockerfile
FROM zauberzeug/nicegui:2.0.0

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN mkdir -p /app/data && chmod -R 777 /app/data

EXPOSE 80

CMD ["python", "main.py"]