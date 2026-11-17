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
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавить товар и увеличить счетчик товарных позиций."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Вернуть описание каждого товара с переводом строки в конце."""
        return "".join(
            f"{product.name}, {product.price} руб. "
            f"Остаток: {product.quantity} шт.\n"
            for product in self.__products
        )
