# Проект: Система учёта метрологического обеспечения

## Stage 1 (MVP) — To-Do Roadmap
**Цель:** Поставить десктоп-клиент и увидеть список equipment из PostgreSQL (read-only).

### A. Базовая инициализация
- [x] Создать репозиторий `metrology` и выложить на GitHub
- [x] Добавить `.gitignore`
- [x] В `pyproject.toml` метаданные (name, version, description)
- [x] Подключить `ruff` (линт+формат) и pre-commit

### B. Зависимости backend (следующий шаг)
- [ ] Установить fastapi, uvicorn, sqlalchemy, psycopg[binary], alembic, pydantic-settings, python-dotenv

---

## Краткие архитектурные заметки
- **Стек:** Tauri + Vue (desktop) → FastAPI (backend) → PostgreSQL (филиальный сервер), BI — Metabase/Superset.
- **Модули:** equipment, verification, status, description, finance, fast_filters, calculation_bar, stat_indicators, authorization, workflow/inbox, documents, forms, arshin_connector, *_history.
- **Особенности:** Approval workflow для лаборантов, хранение истории по годам, интеграция с ФГИС Аршин, генерация типовых форм, загрузка/просмотр документов, e-mail уведомления.
- **Производительность:** индексация по branch/lab/status/date, серверная пагинация, материализованные представления для «истекает/истёк».
- **Эксплуатация:** PgBouncer, бэкапы (pg_dump + WAL), (опц.) standby в филиале, мониторинг.

---

## Прогресс
- Подготовлена рабочая директория, установлен Python 3.13.1, PostgreSQL 17, uv, ruff.
- Инициализирован проект через uv init.
- Настроен pyproject.toml с метаданными.
- Подключен ruff, настроены хуки pre-commit.
- Репозиторий выложен на GitHub (HTTPS remote).

---

## Следующие шаги
1. Установить зависимости backend (FastAPI, SQLAlchemy, Alembic, etc.).
2. Создать базовую структуру backend (`main.py`, `config.py`, `db.py`) и healthcheck.
3. Настроить подключение к PostgreSQL через SQLAlchemy.
4. Инициализировать Alembic и сделать миграцию init.
5. Добавить модель `equipment` и API read-only.
