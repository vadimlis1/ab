"""
Конфигурация сборки пакета ABtool с использованием setuptools.
"""

from setuptools import setup, find_packages

setup(
    name="abtool",
    version="0.1.0",
    description="Веб-сервис для планирования и анализа A/B тестов",
    author="Лисуненко В.Ю., Левашева К.Д.",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.3",
        "flask-cors>=4.0.1",
        "scipy>=1.13.1",
        "gunicorn>=22.0.0",
    ],
    extras_require={
        "docs": [
            "sphinx>=7.3.7",
            "sphinx-rtd-theme>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "abtool=backend.app:main",
        ],
    },
)
