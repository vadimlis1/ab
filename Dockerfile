# ── Этап сборки зависимостей ──────────────────────────────────────
FROM python:3.12-slim AS base

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем и устанавливаем зависимости Python
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ── Финальный образ ───────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Копируем установленные пакеты из этапа сборки
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Копируем исходный код приложения
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY setup.py .

# Переменные окружения
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PORT=5000
ENV PYTHONUNBUFFERED=1

# Открываем порт приложения
EXPOSE 5000

# Запускаем приложение через gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "backend.app:app"]
