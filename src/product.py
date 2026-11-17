"""Товар интернет-магазина."""


class Product:
    """Товар с названием, описанием, ценой и остатком."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        """Создать товар по переданным параметрам."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
