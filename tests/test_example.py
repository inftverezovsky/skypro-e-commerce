"""Запуск точного учебного примера и проверка локального main.py."""

import ast
import hashlib
import runpy
from pathlib import Path

from src.category import Category
from src.product import Product

EXAMPLE = Path(__file__).parent / "examples" / "14.2_main.py.txt"
EXAMPLE_SHA256 = (
    "c57c24aca79980628473d6c793d648b1c3c962d770c7e4cee16154be7d128381"
)


def test_exact_course_example(capsys):
    """Оригинал выполняется без изменений с предоставленными классами."""
    assert hashlib.sha256(EXAMPLE.read_bytes()).hexdigest() == EXAMPLE_SHA256
    namespace = runpy.run_path(
        str(EXAMPLE),
        init_globals={"Product": Product, "Category": Category},
        run_name="__main__",
    )

    assert namespace["category1"].name == "Смартфоны"
    assert Category.category_count == 1
    assert Category.product_count == 4
    assert namespace["new_product"].price == 800
    assert capsys.readouterr().out.splitlines()[-5:] == [
        "800",
        "Цена не должна быть нулевая или отрицательная",
        "800",
        "Цена не должна быть нулевая или отрицательная",
        "800",
    ]


def test_main_keeps_example_behavior():
    """Форматирование и импорты не меняют исполняемый код примера."""
    main_path = Path(__file__).parents[1] / "main.py"
    main_tree = ast.parse(main_path.read_text(encoding="utf-8"))
    example_tree = ast.parse(EXAMPLE.read_text(encoding="utf-8"))

    assert ast.dump(main_tree.body[-1]) == ast.dump(example_tree.body[0])
