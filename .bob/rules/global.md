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

## Bob Shell Headless — Flags Confirmados (Smoke Test 2026-09-25)

BOB_SHELL_CONFIRMED_FLAGS: bob run "<prompt>" -f json --mode ask
BOB_SHELL_ENV_VAR: BOB_API_KEY
BOB_SHELL_MODE_RUNTIME: ask (read-only, seguro, ~0.012 Bobcoins/llamada)
BOB_SHELL_PARSE: doble json.loads() sobre campo last_message
REGLA: nunca usar --mode agent en runtime de PRism

Doble parseo obligatorio en Python:
```python
outer = json.loads(cli_output)
inner = json.loads(outer["last_message"])
findings = inner.get("findings", [])
```

### Métricas de rendimiento medidas
- Costo por llamada: ~0.012 Bobcoins
- Duración promedio: 1.6s – 3.7s por llamada
- Con 4 agentes en modo ECO (secuencial): ~6.4s – 14.8s total, ~0.048 Bobcoins
- Con 4 agentes en modo FULL (paralelo): ~3.7s total, ~0.048 Bobcoins
- Presupuesto de 40 Bobcoins alcanza para ~833 revisiones completas

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
return outer["last_message"]  # string JSON escapado — parsear en _parse_findings()
```

## Formato de Respuesta de Agentes
Cada agente debe responder con este JSON y nada más (sin markdown, sin texto extra):
```json
[
  {
    "severity": "critical|medium|low",
    "title": "Titulo corto del finding",
    "description": "Descripcion detallada con contexto",
    "file": "ruta/al/archivo.py",
    "line": 42
  }
]
```
Los campos `file` y `line` son opcionales si no aplican.
