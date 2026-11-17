"""Проверки товаров."""

import pytest

from src.product import Product


@pytest.mark.parametrize(
    "name, description, price, quantity",
    [
        ("Смартфон", "256GB", 180000.0, 5),
        ("Чехол", "Синий", 799.90, 0),
    ],
)
def test_product_initialization(name, description, price, quantity):
    """Конструктор сохраняет все параметры, включая дробную цену."""
    product = Product(name, description, price, quantity)

    assert getattr(product, "name", None) == name
    assert product.description == description
    assert product.price == price
    assert product.quantity == quantity
