from backend.agents.base import BaseAgent

class SecuritySentinel(BaseAgent):
    name = "SecuritySentinel"

    def build_prompt(self, diff: str, context: dict) -> str:
        return (
            "You are a security auditor. Analyze the diff for OWASP Top 10 vulnerabilities, "
            "hardcoded secrets, SQL injection, XSS, SSRF. "
            'Respond ONLY with raw JSON (no markdown): {"findings":[{"severity":"critical|medium|low","title":"...","description":"...","file":"...","line":0}]}. '
            'If no issues, return {"findings":[]}.\n\nDIFF:\n' + diff[:6000]
        )
