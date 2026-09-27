import asyncio
import json
import os
import shutil
from abc import ABC, abstractmethod
from backend.config import settings
from backend.models import AgentResult, Finding, Severity

BOB_PATH = shutil.which("bob") or r"C:\Users\LUCASJARAMILLOAREIZA\AppData\Roaming\npm\bob.cmd"

class BaseAgent(ABC):
    name: str = "base"

    def __init__(self):
        self.settings = settings

    @abstractmethod
    def build_prompt(self, diff: str, context: dict) -> str:
        pass

    async def analyze(self, diff: str, context: dict, mode: str = "eco") -> AgentResult:
        result = AgentResult(agent_name=self.name, status="running")
        try:
            prompt = self.build_prompt(diff, context)
            raw = await self._call_bob(prompt)
            result.findings = self._parse_findings(raw)
            result.status = "done"
        except Exception as e:
            result.status = "error"
            result.error = str(e)[:500]
        return result

    async def _call_bob(self, prompt: str) -> str:
        env = {**os.environ, "BOB_API_KEY": self.settings.BOB_API_KEY}
        proc = await asyncio.create_subprocess_exec(
            BOB_PATH, "run", prompt, "-f", "json", "--mode", self.settings.BOB_CHAT_MODE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=self.settings.BOB_MAX_TIMEOUT_SECONDS
            )
        except asyncio.TimeoutError:
            proc.kill()
            raise RuntimeError("Bob Shell timeout")
        if proc.returncode != 0:
            raise RuntimeError(f"Bob Shell failed: {stderr.decode()[:200]}")
        output = stdout.decode()
        import sys
        print(f"[BOB RAW] agent={self.name} output={output[:300]}", file=sys.stderr, flush=True)
        return output

    def _parse_findings(self, cli_output: str) -> list[Finding]:
        try:
            outer = json.loads(cli_output)
        except json.JSONDecodeError:
            return [Finding(severity=Severity.low, agent=self.name,
                            title="Unparseable CLI output", description=cli_output[:500])]
        last = outer.get("last_message", "")
        text = last if isinstance(last, str) else json.dumps(last)
        text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            inner = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return [Finding(severity=Severity.low, agent=self.name,
                            title="Unparseable response", description=text[:500])]
        raw_findings = inner.get("findings", []) if isinstance(inner, dict) else []
        findings = []
        for f in raw_findings:
            try:
                findings.append(Finding(
                    severity=Severity(f.get("severity", "low")),
                    agent=self.name,
                    title=f.get("title", "Untitled")[:200],
                    description=f.get("description", "")[:1000],
                    file=f.get("file"),
                    line=f.get("line"),
                ))
            except Exception:
                continue
        return findings
