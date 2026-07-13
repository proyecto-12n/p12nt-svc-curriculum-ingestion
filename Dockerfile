FROM python:3.14-slim AS builder

WORKDIR /app
# Instalar uv a traves de pip
RUN pip install --no-cache-dir uv
COPY pyproject.toml .
# Instalar dependencias en el sistema del builder usando uv como modulo de python
RUN python -m uv pip install --no-cache --system -r pyproject.toml

FROM python:3.14-slim AS runner
WORKDIR /app
# Copiar dependencias de Python instaladas desde la etapa de compilacion
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY ./app ./app

ENV PYTHONPATH=/app:/app/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
