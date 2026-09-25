# PRism — Smoke Test Log (Fase 0.5)

## Resultado: EXITOSO ✅

**Fecha:** 2026-09-25
**Propósito:** Validar Bob Shell headless antes de comprometer Bobcoins al plan

---

## Comando Funcional Confirmado

```bash
bob run "<prompt>" -f json --mode ask
```

Variable de entorno: `BOB_API_KEY`

---

## Métricas Medidas

| Métrica | Valor |
|---|---|
| Costo por llamada (modo ask, prompt corto) | ~0.012384 Bobcoins |
| Duración mínima | 1.6s |
| Duración máxima | 3.7s |
| Modo probado | `ask` |
| Resultado | JSON parseable ✅ |

---

## Formato de Output de Bob Shell

Bob Shell devuelve un JSON con la siguiente estructura:

```json
{
  "type": "...",
  "status": "...",
  "stats": { ... },
  "last_message": "{\"findings\": [...]}"
}
```

⚠️ **CRÍTICO:** `last_message` es un STRING que contiene JSON escapado.
Requiere doble parseo en Python:

```python
outer = json.loads(cli_output)           # parseo 1: envelope de Bob Shell
inner = json.loads(outer["last_message"]) # parseo 2: contenido del agente
findings = inner.get("findings", [])
```

---

## Flags Confirmados

| Flag | Valor | Estado |
|---|---|---|
| Subcomando | `run` | ✅ Confirmado |
| Formato de salida | `-f json` | ✅ Confirmado |
| Modo | `--mode ask` | ✅ Confirmado |
| Variable de entorno | `BOB_API_KEY` | ✅ Confirmado |
| `--mode agent` en runtime | PROHIBIDO | 🚫 Read-only policy |

---

## Decisión de Arquitectura

Los 4 subagentes de PRism **siempre** corren con `--mode ask` porque:
- Es read-only (no puede escribir archivos ni ejecutar comandos)
- Es el modo más barato (~0.012 Bobcoins por llamada)
- Agent mode puede modificar archivos — inaceptable para un sistema de análisis

`--mode agent` queda reservado exclusivamente para sesiones de desarrollo en Bob IDE.

---

## Proyección de Presupuesto (recalibrada)

| Escenario | Costo |
|---|---|
| 1 revisión completa (4 agentes) | ~0.048 Bobcoins |
| Presupuesto total disponible | 40 Bobcoins |
| Revisiones posibles con 40 Bobcoins | ~833 revisiones |
| Estimaciones del plan v3.1 | Muy conservadoras — presupuesto es holgado |
