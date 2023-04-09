FROM python:3.10.11-slim

WORKDIR /app

COPY pyproject.toml .

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && pip install poetry && poetry install

COPY . .

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]