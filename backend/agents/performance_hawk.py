from backend.agents.base import BaseAgent

class PerformanceHawk(BaseAgent):
    name = "PerformanceHawk"

    def build_prompt(self, diff: str, context: dict) -> str:
        return (
            "You are a performance auditor. Detect N+1 queries, nested loops O(n^2), "
            "blocking I/O in async code, expensive calls in hot paths. "
            'Respond ONLY with raw JSON (no markdown): {"findings":[{"severity":"critical|medium|low","title":"...","description":"...","file":"...","line":0}]}. '
            'If no issues, return {"findings":[]}.\n\nDIFF:\n' + diff[:6000]
        )
