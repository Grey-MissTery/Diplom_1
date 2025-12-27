## Задание 1: Юнит-тесты

### Автотесты для проверки программы, которая помогает заказать бургер в Stellar Burgers

### Реализованные сценарии

Созданы юнит-тесты, покрывающие классы `Bun`, `Burger`, `Ingredient`, `Database`

### Тестовое покрытие

- Общее покрытие кода: 94%
- Запуск тестов с генерацией отчета: `pytest --cov=. --cov-report=html`
- Отчет доступен в папке `htmlcov/`

### Структура проекта

```bash
Diplom_1/                    # Корневая директория проекта
├── htmlcov/                 # Отчет о покрытии тестами (генерируется)
├── praktikum/               # Пакет с основной бизнес-логикой
│   ├── __init__.py
│   ├── bun.py
│   ├── burger.py
│   ├── database.py
│   ├── ingredient.py
│   └── ingredient_types.py
├── tests/                   # Пакет с тестами
│    ├── __init__.py
│    ├── test_bun.py        # Тесты для Bun
│    ├── test_burger.py     # Тесты для Burger
│    ├── test_database.py   # Тесты для Database
│    └── test_ingredient.py # Тесты для Ingredient
├── .gitignore              # Исключения для Git
├── conftest.py             # Фикстуры для pytest
├── data.py                 # Тестовые данные
├── praktikum.py            # Основной скрипт
├── README.md               # Документация
└── requirements.txt        # Зависимости Python
```

### Запуск автотестов

> `$ pytest`

**Установка зависимостей**

> `$ pip install -r requirements.txt`
