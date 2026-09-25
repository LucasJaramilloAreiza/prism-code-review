from backend.agents.base import BaseAgent
import json

class LogicAuditor(BaseAgent):
    name = "LogicAuditor"

    def build_prompt(self, diff: str, context: dict) -> str:
        issue = context.get("issue", {})
        issue_text = json.dumps(issue)[:1500] if issue else "No issue linked"
        return (
            "You are a logic auditor. Compare the diff against the issue acceptance criteria. "
            "Flag missing requirements, edge cases, or regressions. "
            'Respond ONLY with raw JSON (no markdown): {"findings":[{"severity":"critical|medium|low","title":"...","description":"...","file":"...","line":0}]}. '
            "If no issues, return {\"findings\":[]}.\n\nISSUE:\n" + issue_text + "\n\nDIFF:\n" + diff[:6000]
        )
