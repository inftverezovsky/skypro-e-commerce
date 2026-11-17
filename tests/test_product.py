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


def test_price_is_private_and_readable():
    """Начальная цена хранится приватно и доступна через свойство."""
    product = Product("Чехол", "Синий", 799.90, 10)

    assert "price" not in vars(product)
    assert product.price == product._Product__price == 799.90
    assert isinstance(Product.price, property)


@pytest.mark.parametrize("new_price", [0.01, 500.0, 1800.0, 799.90])
def test_price_setter_accepts_positive_values(new_price, capsys):
    """Любая положительная цена сохраняется без запроса подтверждения."""
    product = Product("Чехол", "Синий", 799.90, 10)

    product.price = new_price

    assert product.price == new_price
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("new_price", [0, -100.0])
def test_price_setter_rejects_nonpositive_values(new_price, capsys):
    """Неверная цена не сохраняется и сопровождается точным сообщением."""
    product = Product("Чехол", "Синий", 799.90, 10)

    product.price = new_price

    assert product.price == 799.90
    assert capsys.readouterr().out == (
        "Цена не должна быть нулевая или отрицательная\n"
    )


def test_new_product_from_dictionary():
    """Класс-метод возвращает новый товар без изменения исходных данных."""
    data = {
        "name": "Наушники",
        "description": "Беспроводные",
        "price": 1999.50,
        "quantity": 3,
    }
    original = data.copy()

    product = Product.new_product(data)

    assert isinstance(product, Product)
    assert product.name == "Наушники"
    assert product.description == "Беспроводные"
    assert product.price == 1999.50
    assert product.quantity == 3
    assert data == original
    assert isinstance(Product.__dict__["new_product"], classmethod)


def test_new_product_creates_independent_instances():
    """Два вызова фабрики не возвращают один и тот же объект."""
    data = {"name": "Кабель", "description": "USB", "price": 80, "quantity": 0}

    first = Product.new_product(data)
    second = Product.new_product(data)
    first.price = 100

    assert first is not second
    assert second.price == 80
    assert second.quantity == 0


def test_price_setter_returns_none():
    """Успешное изменение цены не возвращает дополнительного результата."""
    product = Product("Кабель", "USB", 80, 15)

    assert Product.price.fset(product, 100) is None
    assert product.price == 100


@pytest.mark.parametrize(
    "price, quantity, expected",
    [
        (80, 15, "Кабель, 80 руб. Остаток: 15 шт."),
        (1999.50, 0, "Кабель, 1999.5 руб. Остаток: 0 шт."),
    ],
)
def test_product_string(price, quantity, expected):
    """Строка товара содержит цену и остаток без перевода строки."""
    product = Product("Кабель", "USB", price, quantity)

    assert str(product) == expected


@pytest.mark.parametrize(
    "price_a, quantity_a, price_b, quantity_b, expected",
    [
        (100, 10, 200, 2, 1400),
        (10.5, 2, 19.99, 3, 80.97),
        (100, 0, 200, 2, 400),
        (100, 0, 200, 0, 0),
        (0.01, 1, 0.01, 1, 0.02),
    ],
)
def test_addition_returns_combined_stock_value(
    price_a, quantity_a, price_b, quantity_b, expected
):
    """Оператор складывает стоимости запасов, не меняя исходные товары."""
    first = Product("Первый", "Описание", price_a, quantity_a)
    second = Product("Второй", "Описание", price_b, quantity_b)

    assert first + second == pytest.approx(expected)
    assert second + first == pytest.approx(expected)
    assert (first.price, first.quantity) == (price_a, quantity_a)
    assert (second.price, second.quantity) == (price_b, quantity_b)


def test_product_string_reflects_changes():
    """Строка товара использует текущую цену и текущий остаток."""
    product = Product("Кабель", "USB", 80, 15)
    product.price = 100
    product.quantity = 0

    assert str(product) == "Кабель, 100 руб. Остаток: 0 шт."
