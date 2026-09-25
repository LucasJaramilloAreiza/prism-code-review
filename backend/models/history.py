from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

class HistoryEntry(BaseModel):
    id: str
    pr_url: str
    pr_title: str = ""
    mode: Literal["eco", "full"] = "eco"
    critical_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
