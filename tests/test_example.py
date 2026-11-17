"""Запуск точного учебного примера и проверка локального main.py."""

import ast
import hashlib
import runpy
from pathlib import Path

from src.category import Category
from src.product import Product

EXAMPLE = Path(__file__).parent / "examples" / "15.1_main.py.txt"
EXAMPLE_SHA256 = (
    "a3583c54d4c389386dd307d363daaf42445452f4b9936b2c2dd22566055adf1e"
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
    assert Category.product_count == 3
    assert str(namespace["category1"]) == (
        "Смартфоны, количество продуктов: 27 шт."
    )
    assert capsys.readouterr().out.splitlines()[-3:] == [
        "2580000.0", "1334000.0", "2114000.0"
    ]


def test_previous_course_example(capsys):
    """Пример 14.2 продолжает работать после добавления магических методов."""
    previous = Path(__file__).parent / "examples" / "14.2_main.py.txt"
    expected_hash = (
        "c57c24aca79980628473d6c793d648b1c3c962d770c7e4cee16154be7d128381"
    )
    assert hashlib.sha256(previous.read_bytes()).hexdigest() == expected_hash
    namespace = runpy.run_path(
        str(previous),
        init_globals={"Product": Product, "Category": Category},
        run_name="__main__",
    )

    assert namespace["new_product"].price == 800
    assert Category.product_count == 4
    assert Category.category_count == 1
    output = capsys.readouterr().out
    assert output.count("Цена не должна быть нулевая или отрицательная") == 2


def test_main_keeps_example_behavior():
    """Форматирование и импорты не меняют исполняемый код примера."""
    main_path = Path(__file__).parents[1] / "main.py"
    main_tree = ast.parse(main_path.read_text(encoding="utf-8"))
    example_tree = ast.parse(EXAMPLE.read_text(encoding="utf-8"))

    assert ast.dump(main_tree.body[-1]) == ast.dump(example_tree.body[0])
