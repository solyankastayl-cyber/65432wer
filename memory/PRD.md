# Fractal Index Platform PRD

## Original Problem Statement
Развёртывание проекта из GitHub репозитория https://github.com/solyankastayl-cyber/765434567
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

### Session 1: Deployment (2026-02-28)
- Развёртывание из GitHub
- TypeScript backend + Python proxy настроены
- Cold Start bootstrap для SPX/DXY/BTC данных
- FRED API ключ установлен
- Все модули зарегистрированы и работают

### Session 2: SPX Page Redesign (2026-03-01)
- **Переключен роут /fractal/spx на SpxFractalPage** (ранее использовался старый FractalPage)
- **Исправлен парсинг API данных** - horizons теперь правильно читается как массив
- **Добавлены недостающие хелперы**: getSentimentDot, getSentimentText
- **Визуал SPX = визуал DXY**:
  - Header Strip: Signal, Confidence, Risk, Phase, As of, REAL badge
  - SPX Verdict Card с dropdown горизонтов
  - Market State, Directional Bias, Expected (P50), Range, Position Size
  - "What would change this view" секция
  - Chart tabs: Synthetic, Replay, Hybrid, Macro ★
  - Forecast by Horizon таблица
  - Risk Context блок
  - Historical Analogs таблица

## API Endpoints (Работающие)
- GET /api/health - Health check
- GET /api/fractal/spx - SPX fractal data
- GET /api/ui/fractal/dxy/overview - DXY данные
- GET /api/fractal/signal - BTC данные
- GET /api/brain/v2/status - Brain status

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Deployment из GitHub
- [x] TypeScript backend запуск
- [x] MongoDB подключение
- [x] FRED API интеграция
- [x] SPX страница приведена к формату DXY

### P1 (High Priority)
- [ ] Динамические invalidations для "What would change this view"
- [ ] Полировка Macro режима для SPX

### P2 (Medium Priority)
- [ ] Оптимизация загрузки Macro Brain
- [ ] Mobile responsive improvements

## Next Tasks
1. Детальная полировка SPX (по запросу пользователя)
2. Любые дополнительные доработки логики фракталов
