# PRism — Bob Project Rules

## Contexto del Proyecto
PRism es un orquestador multi-agente de revisión de Pull Requests.
IBM Bob Shell es el motor de inferencia de los 4 agentes en runtime.

## Reglas de Respuesta
- Responder siempre con JSON estricto cuando se pida análisis de código.
- Nunca incluir markdown (```) alrededor del JSON en respuestas de análisis.
- Si el output debe ser JSON, comenzar directamente con `[` o `{`.

## Reglas de Findings
- Respetar `MAX_FINDINGS = 30` por revisión completa.
- Si hay más de 30 findings, mantener los 10 más críticos ordenados por severidad.
- Severidades válidas: `critical`, `medium`, `low` (siempre en minúsculas).

## Reglas de Diff
- Truncar diffs a 200 líneas en modo ECO.
- Truncar diffs a 4000 líneas en modo FULL.

## Reglas de Seguridad
- Nunca incluir credenciales en respuestas ni en código generado.
- Nunca loguear el valor de BOB_API_KEY.
- Ante 2 fallos consecutivos de invocación de Bob Shell, retornar AgentResult con status `error`.
- **REGLA CRÍTICA:** Nunca usar `--mode agent` en el runtime de PRism.
  Agent mode puede modificar archivos y ejecutar comandos — peligroso para un sistema
  de solo lectura. Reservar agent mode únicamente para el desarrollo con Bob IDE.

## Bob Shell — Flags Confirmados (Fase 0.5 completada)

### Comando de invocación
```bash
bob run "<prompt>" -f json --mode ask
```

### Variable de entorno
- Nombre correcto: `BOB_API_KEY` (NO `BOBSHELL_API_KEY`)
- Se pasa como variable de entorno al proceso subprocess

### Modo confirmado
- `--mode ask` ✅ CONFIRMADO — read-only, seguro, ~0.012 Bobcoins por llamada
- `--mode agent` ❌ PROHIBIDO en runtime — puede modificar archivos
- `--mode plan` — no probado, no necesario para PRism

### Métricas de rendimiento medidas
- Costo por llamada: ~0.012 Bobcoins (llamadas cortas en modo ask)
- Duración promedio: 1.6s – 3.7s por llamada
- Con 4 agentes en modo ECO (secuencial): ~6.4s – 14.8s total, ~0.048 Bobcoins
- Con 4 agentes en modo FULL (paralelo): ~3.7s – 3.7s total, ~0.048 Bobcoins

### Formato de salida de Bob Shell
Bob devuelve un JSON con la siguiente estructura:
```json
{
  "type": "...",
  "status": "...",
  "stats": { ... },
  "last_message": "<STRING JSON ESCAPADO>"
}
```
⚠️ **IMPORTANTE:** El campo `last_message` es un STRING que contiene JSON escapado.
Requiere **doble parseo** en Python:
```python
outer = json.loads(bob_output)           # parseo 1: estructura de Bob Shell
inner = json.loads(outer["last_message"]) # parseo 2: JSON del agente (findings)
```

### Implementación en BaseAgent._call_bob()
```python
proc = await asyncio.create_subprocess_exec(
    "bob", "run", prompt, "-f", "json", "--mode", "ask",
    env={**os.environ, "BOB_API_KEY": settings.BOB_API_KEY},
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
)
stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=settings.BOB_MAX_TIMEOUT_SECONDS)
outer = json.loads(stdout.decode())
return outer["last_message"]  # string JSON — se parsea en _parse_findings()
```

## Calibración de Presupuesto Actualizada
- Costo real por agente: ~0.012 Bobcoins
- Costo por revisión completa (4 agentes): ~0.048 Bobcoins
- Presupuesto de 40 Bobcoins alcanza para ~833 revisiones completas
- Estimaciones del plan v3.1 eran conservadoras — el presupuesto es holgado

## Formato de Respuesta de Agentes
Cada agente debe responder con este JSON y nada más (sin markdown, sin texto extra):
```json
[
  {
    "severity": "critical|medium|low",
    "title": "Título corto del finding",
    "description": "Descripción detallada con contexto",
    "file": "ruta/al/archivo.py",
    "line": 42
  }
]
```
Los campos `file` y `line` son opcionales si no aplican.
