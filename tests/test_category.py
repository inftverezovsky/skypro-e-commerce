"""Проверки категорий и общих счетчиков."""

import pytest

from src.category import Category
from src.product import Product


def test_category_initialization(sample_products):
    """Конструктор сохраняет название, описание и объекты товаров."""
    category = Category("Техника", "Товары для дома", sample_products)

    assert getattr(category, "name", None) == "Техника"
    assert category.description == "Товары для дома"
    assert category._Category__products == sample_products


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

    assert empty.products == ""
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_standalone_product_does_not_change_category_counters():
    """Товар вне категории не меняет общие счетчики категорий."""
    Product("Чехол", "Синий", 800.0, 10)

    assert Category.product_count == 0
    assert Category.category_count == 0


def test_products_getter_is_read_only_text(category, sample_products):
    """Геттер показывает товары строкой, не раскрывая приватный список."""
    assert category.products == (
        "Смартфон, 180000.0 руб. Остаток: 5 шт.\n"
        "Чехол, 799.9 руб. Остаток: 10 шт.\n"
    )
    assert "products" not in vars(category)
    assert category._Category__products == sample_products
    with pytest.raises(AttributeError):
        category.products = []


def test_add_product_appends_and_counts(category):
    """Добавление сохраняет объект и увеличивает счетчик ровно на один."""
    product = Product("Телевизор", "4K", 123000.0, 7)
    other = Category("Пустая", "Для проверки общих счетчиков", [])

    result = category.add_product(product)

    assert category._Category__products[-1] is product
    assert category.products.endswith(
        "Телевизор, 123000.0 руб. Остаток: 7 шт.\n"
    )
    assert result is None
    assert Category.product_count == other.product_count == 3
    assert Category.category_count == 2


def test_add_product_to_empty_category():
    """Первый товар появляется в пустой категории и общем счетчике."""
    empty = Category("Пустая", "Без товаров", [])
    product = Product("Кабель", "USB", 80, 15)

    assert empty.add_product(product) is None
    assert empty.products == "Кабель, 80 руб. Остаток: 15 шт.\n"
    assert Category.product_count == 1


def test_products_getter_uses_current_values(category, sample_products):
    """Геттер не кэширует устаревшую цену или остаток товара."""
    sample_products[0].price = 800
    sample_products[0].quantity = 0

    assert category.products.startswith(
        "Смартфон, 800 руб. Остаток: 0 шт.\n"
    )


@pytest.mark.parametrize(
    "quantities, expected", [([], 0), ([5, 10], 15), ([0, 2], 2)]
)
def test_category_string_counts_stock(quantities, expected):
    """Строка категории считает только ее остатки, не товарные позиции."""
    products = [
        Product(f"Товар {index}", "Описание", 80, quantity)
        for index, quantity in enumerate(quantities)
    ]
    category = Category("Техника", "Первая категория", products)
    Category("Другая", "Чужие товары", [Product("Чужой", "Описание", 1, 999)])

    assert str(category) == f"Техника, количество продуктов: {expected} шт."


def test_category_string_reflects_stock_changes(category, sample_products):
    """Строка обновляется после добавления товара и изменения остатка."""
    category.add_product(Product("Телевизор", "4K", 123000.0, 7))
    assert str(category) == "Техника, количество продуктов: 22 шт."

    sample_products[0].quantity = 3
    assert str(category) == "Техника, количество продуктов: 20 шт."
    assert Category.product_count == 3
