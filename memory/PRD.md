# Fractal Index Platform PRD

## Original Problem Statement
Развёртывание проекта из GitHub репозитория https://github.com/solyankastayl-cyber/Finalll23
- Модуль фракталов для валютных пар (DXY) - основной фокус разработки
- SPX и Bitcoin логика (в заморозке - поднять без изменений)
- Админка
- FRED API для макроданных: 2c0bf55cfd182a3a4d2e4fd017a622f7

## Architecture
- **Backend**: TypeScript/Fastify на порту 8002, Python proxy на 8001
- **Frontend**: React на порту 3000
- **Database**: MongoDB
- **External APIs**: FRED API для макроданных

## User Personas
1. **Трейдер/Аналитик** - использует DXY/SPX/BTC терминалы для прогнозов
2. **Администратор** - управляет системой через админку

## Core Requirements (Static)
- DXY Fractal Terminal с режимами: Synthetic, Replay, Hybrid, Macro
- SPX Fractal Terminal с аналогичными режимами
- BTC Fractal Terminal (заморожен)
- Macro Brain v4 - агрегация макро-данных
- Admin Panel с авторизацией

## What's Been Implemented

### Session 1: Deployment (2026-03-01)
- Клонирование из GitHub репозитория
- TypeScript backend + Python proxy настроены
- Cold Start bootstrap для SPX/DXY/BTC данных из CSV
- FRED API ключ установлен
- Все модули зарегистрированы и работают:
  - BTC Terminal: /api/btc/v2.1/*
  - SPX Terminal: /api/spx/v2.1/*
  - DXY Module: /api/fractal/dxy/*
  - Brain v2: /api/brain/v2/*
  - Index Engine V2: /api/v2/index/*
  - Admin Auth: /api/admin/*
  - И многие другие модули

### Тестирование (2026-03-01)
- Backend: 71.4% тестов пройдено (10/14)
- Frontend: 100% страниц загружаются корректно
- Основные API работают:
  - /api/health - OK
  - /api/fractal/signal - BTC NEUTRAL signal
  - /api/ui/fractal/dxy/overview - USD_UP verdict, +5.18%
  - /api/fractal/spx - LONG signal, DISTRIBUTION phase
  - /api/brain/v2/status - ACTIVE

## API Endpoints (Работающие)
- GET /api/health - Health check
- GET /api/fractal/signal - BTC fractal signal
- GET /api/ui/fractal/dxy/overview - DXY данные
- GET /api/fractal/spx - SPX данные
- GET /api/brain/v2/status - Brain status
- GET /api/v2/index/:symbol/pack - Index Engine
- GET /api/system/health - System health

## Known Issues (Low Priority)
1. WebSocket connections failing (/api/ws, /ws) - real-time updates affected
2. Some alternative endpoints 404 (focus pack routes) - main APIs work
3. Brain dashboard loading time ~15 seconds

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Deployment из GitHub
- [x] TypeScript backend запуск
- [x] MongoDB подключение
- [x] FRED API интеграция
- [x] Cold Start bootstrap данных

### P1 (High Priority)
- [ ] Исправить WebSocket соединения для real-time обновлений
- [ ] Полировка Macro режима для DXY

### P2 (Medium Priority)
- [ ] Оптимизация загрузки Macro Brain
- [ ] Mobile responsive improvements

## Next Tasks
1. Доработки модуля фракталов DXY (по запросу пользователя)
2. Исправление WebSocket (если нужны real-time обновления)
3. Любые дополнительные доработки логики
