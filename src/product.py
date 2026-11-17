"""Товар интернет-магазина."""


class Product:
    """Товар с названием, описанием, ценой и остатком."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        """Создать товар по переданным параметрам."""
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """Создать товар из словаря с его четырьмя основными полями."""
        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"],
        )

    @property
    def price(self) -> float:
        """Вернуть текущую цену товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Обновить цену, только если новое значение положительно."""
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")
