from datetime import datetime
from enum import Enum
from typing import Literal, Optional
from pydantic import BaseModel, Field

class Severity(str, Enum):
    critical = "critical"
    medium = "medium"
    low = "low"

class Finding(BaseModel):
    severity: Severity
    agent: str
    title: str
    description: str
    file: Optional[str] = None
    line: Optional[int] = None

class AgentResult(BaseModel):
    agent_name: str
    status: Literal["pending", "running", "done", "error"] = "pending"
    findings: list[Finding] = Field(default_factory=list)
    error: Optional[str] = None

class ReviewRequest(BaseModel):
    pr_url: str
    mode: Literal["eco", "full"] = "eco"

class Report(BaseModel):
    id: str
    pr_url: str
    pr_title: str = ""
    mode: Literal["eco", "full"] = "eco"
    agents: list[AgentResult] = Field(default_factory=list)
    summary: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
