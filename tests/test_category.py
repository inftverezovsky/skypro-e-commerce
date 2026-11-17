"""Проверки категорий и общих счетчиков."""

from src.category import Category
from src.product import Product


def test_category_initialization(sample_products):
    """Конструктор сохраняет название, описание и объекты товаров."""
    category = Category("Техника", "Товары для дома", sample_products)

    assert getattr(category, "name", None) == "Техника"
    assert category.description == "Товары для дома"
    assert category.products == sample_products


def test_category_count_is_shared(sample_products):
    """Создание каждой категории увеличивает общий счетчик категорий."""
    first = Category("Техника", "Первая категория", sample_products)
    assert Category.category_count == 1

    second = Category("Пустая", "Вторая категория", [])
    assert Category.category_count == 2
    assert first.category_count == second.category_count == 2


def test_product_count_counts_positions(sample_products):
    """Счетчик суммирует позиции категорий, а не остатки на складе."""
    first = Category("Техника", "Первая категория", sample_products)
    assert Category.product_count == 2

    second = Category("Аксессуары", "Вторая категория", sample_products[:1])
    assert first.product_count == second.product_count == 3

    Category("Пустая", "Без товаров", [])
    assert Category.product_count == 3


def test_empty_category():
    """Пустая категория допустима и не добавляет товарных позиций."""
    empty = Category("Пустая", "Без товаров", [])

    assert empty.products == []
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_standalone_product_does_not_change_category_counters():
    """Товар вне категории не меняет общие счетчики категорий."""
    Product("Чехол", "Синий", 800.0, 10)

    assert Category.product_count == 0
    assert Category.category_count == 0
