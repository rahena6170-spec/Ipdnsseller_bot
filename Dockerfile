FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir pyTelegramBotAPI requests flask gunicorn

COPY . /app

CMD ["python", "Main.py"]
