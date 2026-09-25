# PRism — Multi-Agent Code Review Orchestrator

> IBM Bob 2.0 Hackathon Entry

PRism analyzes GitHub Pull Requests using **four specialized AI agents** powered by **IBM Bob Shell**, and delivers a prioritized risk panel (🔴 Critical / 🟡 Medium / 🟢 Low) in real time.

## Architecture

```
PR URL → GitHub API (diff + linked issue)
              ↓
         Orchestrator
    ┌─────────────────────┐
    │  Security Sentinel  │  OWASP Top 10, secrets, injections
    │  Logic Auditor      │  Acceptance criteria vs. code
    │  Performance Hawk   │  N+1, O(n²), blocking calls
    │  Blast-Radius Mapper│  Downstream impact analysis
    └─────────────────────┘
              ↓
      Risk Panel (WebSocket streaming)
```

Each agent is powered by `bob --auth-method api-key -p "<prompt>" --chat-mode ask`.

## Quick Start

```bash
cp .env.example .env
# Edit .env and add your BOBSHELL_API_KEY and GITHUB_TOKEN
docker-compose up --build
```

Open http://localhost:3000

## Required Environment Variables

| Variable | Description |
|---|---|
| `BOBSHELL_API_KEY` | Bob Inference API Key from bob.ibm.com → Settings → API Keys |
| `GITHUB_TOKEN` | GitHub Personal Access Token (repo read scope) |
| `DATABASE_URL` | SQLite path (default: `sqlite:///./prism.db`) |
| `BOB_MAX_TIMEOUT_SECONDS` | Bob Shell subprocess timeout (default: 45) |
| `BOB_CHAT_MODE` | Bob chat mode confirmed in smoke test (default: `ask`) |

## Modes

| Mode | Description | Bobcoins |
|---|---|---|
| **ECO** | Sequential agents, diff ≤200 lines | ~1 per review |
| **FULL** | Parallel agents, full diff | ~4-6 per review |

## Stack

- **Backend:** FastAPI + WebSockets + aiosqlite
- **Frontend:** Next.js 14 + Tailwind CSS + lucide-react
- **AI Engine:** IBM Bob Shell (`--auth-method api-key`)
- **Infrastructure:** Docker Compose

## Bob Sessions

Screenshots of Bob IDE sessions used during development are in `bob_sessions/`.

---

Built for the IBM Bob 2.0 Hackathon.
