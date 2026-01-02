FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project --locked
COPY . .

EXPOSE 8000

CMD ["uvicorn", "fast_auth.app:app", "--host", "0.0.0.0", "--port", "8000"]