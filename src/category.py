"""Категории товаров интернет-магазина."""

from src.product import Product


class Category:
    """Категория товаров с общими счетчиками."""

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: list[Product]
    ) -> None:
        """Создать категорию с переданным списком товаров."""
        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1
        Category.product_count += len(products)
