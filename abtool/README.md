# ABtool — Веб-сервис для A/B тестирования

Инструмент для продуктовых аналитиков: планирование A/B тестов и анализ их результатов в одном месте.

## Команда

| Участник | Роль |
|----------|------|
| Лисуненко В.Ю. | Backend + аналитика |
| Левашева К.Д. | Frontend + аналитика |

## Функционал

- Калькулятор размера выборки (MDE, alpha, power)
- Анализ результатов теста (z-тест, p-value, доверительный интервал, uplift)
- Текстовая интерпретация результата
- История расчётов в браузере

## Структура проекта

```
abtool/
├── backend/
│   ├── app.py            # расчётные функции
│   └── requirements.txt  # зависимости Python
├── frontend/
│   └── index.html        # интерфейс
├── docs/
│   ├── conf.py           # конфигурация Sphinx
│   └── index.rst         # главная страница документации
├── setup.py              # сборка пакета
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Зависимости

```
flask==3.0.3
flask-cors==4.0.1
scipy==1.13.1
gunicorn==22.0.0
```

## Установка и запуск

### Локальная разработка

```bash
# Установить зависимости
pip install -r backend/requirements.txt

# Запустить
python backend/app.py
```

### Установка пакета через setuptools

```bash
pip install -e .
```

### Запуск через Docker Compose

```bash
docker-compose up --build
```

### Сборка документации (Sphinx)

```bash
pip install sphinx sphinx-rtd-theme
cd docs
sphinx-apidoc -o . ../backend
make html
# Документация появится в docs/_build/html/index.html
```