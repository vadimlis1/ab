"""
Конфигурация Sphinx для генерации документации проекта ABtool.
"""

import os
import sys

# Добавляем корень проекта в путь, чтобы Sphinx нашёл модуль backend
sys.path.insert(0, os.path.abspath("../backend"))

# -- Информация о проекте --------------------------------------------------
project = "ABtool"
copyright = "2025, Лисуненко В.Ю., Левашева К.Д."
author = "Лисуненко В.Ю., Левашева К.Д."
release = "0.1.0"

# -- Настройки Sphinx -------------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",    # автодокументация из docstrings
    "sphinx.ext.viewcode",   # ссылки на исходный код
    "sphinx.ext.napoleon",   # поддержка Google/NumPy docstring стиля
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]
language = "ru"

# -- Тема оформления --------------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]