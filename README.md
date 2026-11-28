MCP-сервер для автоматизированной обработки результатов статического анализа программного обеспечения.

## О проекте
Цель - разработать программный прототип MCP-сервера для загрузки, нормализации и аналитической обработки результатов SAST с последующим предоставлением этих данных большой языковой модели.

## Текущий этап
8 — Подготовка опытного образца.

Подробнее — в [План работы](docs/plan.md)

## Быстрый старт
```bash
# Клонирование репозитория
git clone -b develop https://github.com/Otto-7/mcp.git
cd MCP-security-server

# Создание окружения в папке с кодом
python -m venv .venv

# Активация для Windows:
.venv\Scripts\activate
# Для Linux/macOS:
source .venv/bin/activate

# Установка зависимостей
pip install fastmcp

# Запуск сервера через терминал 
python server.py --sarif data/input/имя_файла.sarif
# Тестовый файл
python server.py --sarif data/input/zlib-git-master-09a1572.sarif
```
## Подключение к LLM
```bash
# Путь
pwd [home/user/mcp]
# Регистрация сервера
codex mcp add [NAME MCP] -- /[home/user/mcp]/.venv/bin/python /home/user/mcp/Server.py --sarif /home/user/mcp/data/input/zlib-git-master-09a1572.sarif
# Проверка регистрации
codex mcp list
# Запуск
codex
# Проверить, что нейросеть видит сервер
/mcp
# Вставить промт
```

## Документация

- [План работы](docs/plan.md) 
- [Архитектура](docs/architecture.md) 
- [Теоретическая сводка](docs/research/)

## Зависимости
В проекте используется только одна внешняя библиотека:
* **`fastmcp`** — фреймворк для создания MCP-сервера.
