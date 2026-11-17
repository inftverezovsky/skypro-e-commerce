# e-commerce

Учебное ядро интернет-магазина: товары и категории.

## Работа 14.1

- `Product` хранит `name`, `description`, `price` и `quantity`.
- `Category` хранит название, описание и список объектов `Product`.
- `Category.category_count` считает созданные категории.
- `Category.product_count` считает товарные позиции в категориях,
  а не сумму остатков `quantity`. Отдельное создание товара счетчики не меняет.

Код расположен в `src/product.py` и `src/category.py`, тесты — в `tests/`.
Каждый тест изолирует общие счетчики через фикстуру.

## Пример

```bash
poetry run python main.py
```

В `tests/examples/14.1_main.py.txt` сохранен точный текст учебного примера.
Тест проверяет его SHA-256 и выполняет без изменения, предоставляя классы
`Product` и `Category` (в исходном примере импорты отсутствуют).
В корневой `main.py` добавлены импорты и форматирование; равенство
исполняемого AST с исходным примером проверяется тестом.

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
