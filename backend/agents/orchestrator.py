import asyncio
import uuid
from backend.agents.security_sentinel import SecuritySentinel
from backend.agents.logic_auditor import LogicAuditor
from backend.agents.performance_hawk import PerformanceHawk
from backend.agents.blast_radius import BlastRadiusMapper
from backend.models import Report, Finding, Severity
from backend.github.client import GitHubClient

MAX_FINDINGS = 30
TOP_N = 10

class Orchestrator:
    def __init__(self):
        self.gh = GitHubClient()
        self.agents = [
            SecuritySentinel(),
            LogicAuditor(),
            PerformanceHawk(),
            BlastRadiusMapper(),
        ]

    async def run(self, pr_url: str, mode: str, queue: asyncio.Queue, review_id: str | None = None) -> Report:
        report = Report(id=review_id or str(uuid.uuid4()), pr_url=pr_url, mode=mode)
        try:
            details = await self.gh.get_pr_details(pr_url)
            report.pr_title = details.get("title", "")
            diff = await self.gh.get_pr_diff(pr_url, mode=mode)
            issue = await self.gh.get_linked_issue(details["owner"], details["repo"], details["body"])
            context = {"issue": issue, "pr": details}

            await queue.put({"event": "review_started", "review_id": report.id})

            if mode == "eco":
                results = []
                for agent in self.agents:
                    await queue.put({"event": "agent_started", "agent": agent.name})
                    r = await agent.analyze(diff, context, mode)
                    results.append(r)
                    await queue.put({"event": "agent_completed", "agent": agent.name,
                                     "findings_count": len(r.findings),
                                     "findings": [f.model_dump() for f in r.findings]})
            else:
                for agent in self.agents:
                    await queue.put({"event": "agent_started", "agent": agent.name})
                results = await asyncio.gather(*[a.analyze(diff, context, mode) for a in self.agents])
                for r in results:
                    await queue.put({"event": "agent_completed", "agent": r.agent_name,
                                     "findings_count": len(r.findings),
                                     "findings": [f.model_dump() for f in r.findings]})

            report.agents = list(results)
            report = self._apply_guard(report)
            report.summary = self._summarize(report)
            await queue.put({"event": "review_complete", "report": report.model_dump(mode="json")})
        except Exception as e:
            await queue.put({"event": "error", "message": str(e)[:500]})
        return report

    def _apply_guard(self, report: Report) -> Report:
        all_findings = [(a.agent_name, f) for a in report.agents for f in a.findings]
        if len(all_findings) <= MAX_FINDINGS:
            return report
        order = {Severity.critical: 0, Severity.medium: 1, Severity.low: 2}
        all_findings.sort(key=lambda x: order.get(x[1].severity, 3))
        kept = all_findings[:TOP_N]
        truncated = len(all_findings) - TOP_N
        by_agent: dict[str, list] = {}
        for name, f in kept:
            by_agent.setdefault(name, []).append(f)
        for agent in report.agents:
            agent.findings = by_agent.get(agent.agent_name, [])
        if truncated > 0 and report.agents:
            report.agents[0].findings.append(Finding(
                severity=Severity.low, agent="orchestrator",
                title=f"{truncated} additional findings truncated",
                description="Increase TOP_N or review manually."))
        return report

    def _summarize(self, report: Report) -> dict:
        counts = {"critical": 0, "medium": 0, "low": 0}
        for a in report.agents:
            for f in a.findings:
                counts[f.severity.value] += 1
        return counts
