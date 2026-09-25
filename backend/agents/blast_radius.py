from backend.agents.base import BaseAgent

class BlastRadiusMapper(BaseAgent):
    name = "BlastRadiusMapper"

    def build_prompt(self, diff: str, context: dict) -> str:
        return (
            "You are a blast-radius analyst. Identify modules, public APIs, or services "
            "downstream that may break due to the changes in this diff. "
            'Respond ONLY with raw JSON (no markdown): {"findings":[{"severity":"critical|medium|low","title":"...","description":"...","file":"...","line":0}]}. '
            'If no issues, return {"findings":[]}.\n\nDIFF:\n' + diff[:6000]
        )
