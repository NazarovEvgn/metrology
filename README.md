## Быстрый старт
# 1) Бэкенд: .env
cp .env.example .env

# 2) Миграции + запуск API
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 3) Фронтенд: .env
cd metrology-desktop
cp .env.example .env            # VITE_API_BASE=http://127.0.0.1:8000

# 4) Dev: все сразу (API + Tauri)
npm install
npm run dev:all


Минимальный рабочий комплект:
- **Backend**: FastAPI + SQLAlchemy + Alembic + PostgreSQL
- **Desktop/Web**: Vue 3 + Vite + **Tauri v2**
- Модуль **equipment** (read-only): список, детальная запись, поиск и фильтры

## Стек и требования

### Backend
- Python 3.11+ (проекты запускаем через **uv**)
- PostgreSQL 14+ (UTF8)
- Windows: PowerShell

### Desktop/Web
- Node.js LTS (рекомендуем через winget)
- Rust toolchain (**cargo/rustc**, `stable-x86_64-pc-windows-msvc`)
- MSVC Build Tools + Windows SDK
- WebView2 Runtime
