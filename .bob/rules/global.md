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
- Nunca loguear el valor de BOBSHELL_API_KEY.
- Ante 2 fallos consecutivos de invocación de Bob Shell, retornar AgentResult con status `error`.

## Bob Shell — Flags Confirmados
BOB_SHELL_CONFIRMED_FLAGS: <completar en Fase 0.5 con resultado del smoke test>
BOB_INSTALL_METHOD: <completar en Fase 0.5 con método confirmado en Discord>

## Formato de Respuesta de Agentes
Cada agente debe responder con este JSON y nada más:
```
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
