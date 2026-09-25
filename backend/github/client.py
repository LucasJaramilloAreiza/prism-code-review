import re
import httpx
from typing import Optional
from backend.config import settings

GITHUB_API = "https://api.github.com"

class GitHubClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    @staticmethod
    def parse_pr_url(pr_url: str) -> tuple[str, str, int]:
        m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)", pr_url.strip())
        if not m:
            raise ValueError(f"Invalid GitHub PR URL: {pr_url}")
        return m.group(1), m.group(2), int(m.group(3))

    async def get_pr_details(self, pr_url: str) -> dict:
        owner, repo, number = self.parse_pr_url(pr_url)
        url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=self.headers)
            r.raise_for_status()
            data = r.json()
            return {
                "owner": owner,
                "repo": repo,
                "number": number,
                "title": data.get("title", ""),
                "body": data.get("body") or "",
                "state": data.get("state", ""),
                "additions": data.get("additions", 0),
                "deletions": data.get("deletions", 0),
            }

    async def get_pr_diff(self, pr_url: str, mode: str = "eco") -> str:
        owner, repo, number = self.parse_pr_url(pr_url)
        url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{number}"
        headers = {**self.headers, "Accept": "application/vnd.github.v3.diff"}
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.get(url, headers=headers)
            r.raise_for_status()
            diff = r.text
        limit = 200 if mode == "eco" else 4000
        lines = diff.splitlines()
        if len(lines) > limit:
            return "\n".join(lines[:limit]) + f"\n\n[TRUNCATED: {len(lines) - limit} more lines]"
        return diff

    async def get_linked_issue(self, owner: str, repo: str, pr_body: str) -> dict:
        m = re.search(r"(?:Fixes|Closes|Resolves)\s+#(\d+)", pr_body, re.IGNORECASE)
        if not m:
            return self._fallback_issue()
        issue_number = int(m.group(1))
        url = f"{GITHUB_API}/repos/{owner}/{repo}/issues/{issue_number}"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.get(url, headers=self.headers)
                if r.status_code != 200:
                    return self._fallback_issue()
                data = r.json()
                return {
                    "number": data.get("number"),
                    "title": data.get("title", ""),
                    "body": data.get("body") or "",
                    "labels": [l.get("name") for l in data.get("labels", [])],
                }
        except Exception:
            return self._fallback_issue()

    @staticmethod
    def _fallback_issue() -> dict:
        import json
        from pathlib import Path
        path = Path("demo_data/mock_issue.json")
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8-sig"))
        return {"number": 0, "title": "No issue linked", "body": "", "labels": []}
