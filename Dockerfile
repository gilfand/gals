# Dockerfile
FROM zauberzeug/nicegui:2.0.0

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN mkdir -p /app/data

EXPOSE 8080

CMD ["python", "-u", "main.py"]