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

### Session 2: BLOCK 77 - Horizon Meta (2026-03-01)
**Реализовано Adaptive Similarity Weighting + Horizon Hierarchy:**

1. **Divergence Monitor** (`horizon_meta.service.ts`)
   - Отслеживает расхождение real vs predicted
   - Формула: `div = mean_abs(real_return[i] - expected_return[i])`
   - Пороги per-horizon: 30D=1.2%, 90D=1.0%, 180D=0.9%, 365D=0.8%

2. **Confidence Decay** 
   - `decay = exp(-lambda * excess)` где excess = (div - thr) / thr
   - Clamp: [0.35, 1.0] - никогда не падает ниже 35%
   - Не меняет projection, только confidence

3. **Horizon Hierarchy Weighting**
   - Base weights: 30D=15%, 90D=25%, 180D=25%, 365D=35%
   - Effective weights: `wH_eff = wH * confAdj * stability`
   - Normalized to sum = 1.0

4. **Consensus Bias**
   - `consensusBias = Σ (wH_eff * bias_H)`
   - States: BULLISH (>0.25), BEARISH (<-0.25), HOLD (otherwise)
   - Mode: SHADOW (compute but don't apply)

5. **Projection Tracking** (для Live Overlay)
   - Сохранение snapshot'ов прогнозов в MongoDB
   - Deduplication via MD5 hash
   - Endpoint: `/api/fractal/horizon-meta/tracking/:asset/:horizon`

**Новые endpoints:**
- GET `/api/fractal/horizon-meta/config` - конфигурация
- POST `/api/fractal/horizon-meta/config` - обновление config
- GET `/api/fractal/horizon-meta/tracking/:asset/:horizon` - tracking overlay
- POST `/api/fractal/horizon-meta/test` - unit tests

**Тестирование:** 6/8 unit tests passed (100% backend API tests)

## API Endpoints Summary

### DXY Terminal (обновлено)
- GET `/api/fractal/dxy/terminal?focus=90d` - теперь возвращает `horizonMeta` объект

### Horizon Meta
- GET `/api/fractal/horizon-meta/config`
- POST `/api/fractal/horizon-meta/test`

## Known Issues (Low Priority)
1. WebSocket connections failing (/api/ws) - not critical
2. 2/8 unit tests failing due to test data limitations - expected

## Prioritized Backlog

### P0 (Critical) - DONE
- [x] Deployment
- [x] BLOCK 77: Adaptive Similarity + Hierarchy (shadow mode)

### P1 (High Priority)
- [ ] Enable mode='on' для HorizonMeta (после валидации в shadow)
- [ ] Multi-horizon aggregation для consensus
- [ ] Live Tracking Overlay в UI

### P2 (Medium Priority)
- [ ] SPX DXY-Overlay: adjustedSPX = spxHybrid + beta * (-dxyMacro)
- [ ] WebSocket исправление

## Next Tasks
1. Валидация HorizonMeta в shadow mode на реальных данных
2. Включение mode='on' после успешной валидации
3. UI интеграция Live Tracking Overlay
4. SPX Cascade с DXY overlay
