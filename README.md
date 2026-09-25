# PRism — Multi-Agent Code Review Orchestrator

> IBM Bob 2.0 Hackathon Entry

PRism analyzes GitHub Pull Requests using **four specialized AI agents** powered by **IBM Bob Shell**, and delivers a prioritized risk panel (🔴 Critical / 🟡 Medium / 🟢 Low) in real time via WebSocket streaming.

---

## Architecture

```
PR URL → GitHub API (diff + linked issue)
              ↓
         Orchestrator
    ┌─────────────────────────────────────────┐
    │  Security Sentinel   OWASP Top 10, secrets, injections     │
    │  Logic Auditor       Acceptance criteria vs. code          │
    │  Performance Hawk    N+1, O(n²), blocking calls            │
    │  Blast-Radius Mapper Downstream impact analysis            │
    └─────────────────────────────────────────┘
              ↓
      Risk Panel (WebSocket streaming)
```

Each agent is powered by:
```bash
bob run "<prompt>" -f json --mode ask
```
`--mode ask` is read-only and used exclusively in runtime — agent mode is prohibited.

---

## Bob Shell Headless Setup
Instalar: `powershell -ep Bypass 'irm -Uri "https://bob.ibm.com/download/bobshell.ps1" | iex'`
Licencia: `bob --accept-license`
Variable: `$env:BOB_API_KEY="tu_key"`

---

## Docker Quick Start
```bash
cp .env.example .env
# edita .env con tus keys reales
docker-compose up --build
```

---

## Environment Variables
| Variable | Descripción | Requerida |
|---|---|---|
| BOB_API_KEY | Bob Shell API Key (inference) | Sí |
| GITHUB_TOKEN | GitHub PAT para PRs | Sí |
| BOB_CHAT_MODE | ask (default) | No |

---

## Two Modes — ECO / FULL
ECO: modo ask secuencial, diff ≤200 líneas, ~0.05 Bobcoins por revisión.
FULL: modo ask paralelo, diff completo, ~0.20-0.50 Bobcoins por revisión.

---

## Stack

| Layer | Technology |
|---|---|
| AI Engine | IBM Bob Shell (`bob run -f json --mode ask`) |
| Backend | FastAPI + WebSockets + aiosqlite |
| Frontend | Next.js 14 + Tailwind CSS + lucide-react |
| Infrastructure | Docker Compose |
| Database | SQLite (persistent via Docker volume) |

---

## Bob Sessions

Screenshots of Bob IDE sessions used during development are in `bob_sessions/`.
See `demo_data/smoke_test_log.md` for the Fase 0.5 headless validation results.

---

Built for the IBM Bob 2.0 Hackathon.
