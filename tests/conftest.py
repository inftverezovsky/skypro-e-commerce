"""Общие тестовые данные и изоляция счетчиков."""

import pytest

from src.category import Category
from src.product import Product


@pytest.fixture(autouse=True)
def reset_category_counters(monkeypatch):
    """Начать каждый тест с нулевых счетчиков и восстановить их после."""
    monkeypatch.setattr(Category, "category_count", 0)
    monkeypatch.setattr(Category, "product_count", 0)


@pytest.fixture
def sample_products():
    """Вернуть две позиции с остатками больше единицы."""
    return [
        Product("Смартфон", "256GB", 180000.0, 5),
        Product("Чехол", "Синий", 799.90, 10),
    ]


@pytest.fixture
def category(sample_products):
    """Создать категорию для проверок ее поведения."""
    return Category("Техника", "Товары для дома", sample_products)
