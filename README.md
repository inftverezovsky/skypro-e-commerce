# e-commerce

Учебное ядро интернет-магазина: товары и категории.

## Установка

Требуется Python 3.10 или новее и Poetry 2.x.

```bash
poetry install
```

## Разработка

Основные ветки: `main` и `develop`. Каждая домашняя работа хранится
в отдельной ветке `feature/homework_<номер>`.

```bash
poetry run python -m pytest
poetry run python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
poetry run python -m flake8 src tests main.py
poetry run python -m isort --check-only src tests main.py
```

HTML-отчет о покрытии сохраняется в `htmlcov/index.html`.
Порог покрытия — 76%, то есть строго больше 75%.
