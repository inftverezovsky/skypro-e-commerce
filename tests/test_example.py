"""Запуск точного учебного примера и проверка локального main.py."""

import ast
import hashlib
import runpy
from pathlib import Path

from src.category import Category
from src.product import Product

EXAMPLE = Path(__file__).parent / "examples" / "14.1_main.py.txt"
EXAMPLE_SHA256 = (
    "c5e572697558de69324d339b8f151e9b2bb01f787469d1c461ac785ce32d87ce"
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
    assert len(namespace["category1"].products) == 3
    assert Category.category_count == 2
    assert Category.product_count == 4
    assert capsys.readouterr().out.splitlines()[-2:] == ["2", "4"]


def test_main_keeps_example_behavior():
    """Форматирование и импорты не меняют исполняемый код примера."""
    main_path = Path(__file__).parents[1] / "main.py"
    main_tree = ast.parse(main_path.read_text(encoding="utf-8"))
    example_tree = ast.parse(EXAMPLE.read_text(encoding="utf-8"))

    assert ast.dump(main_tree.body[-1]) == ast.dump(example_tree.body[0])
