FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . .

RUN uv sync --package backend

ENV PYTHONPATH=/app/backend

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]