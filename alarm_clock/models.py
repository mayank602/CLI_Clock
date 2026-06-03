from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


@dataclass
class Alarm:
    id: str
    time_iso: str
    label: str = ""
    recurrence: Optional[str] = None  # None, 'daily', 'weekly'
    days: Optional[List[int]] = None  # for weekly: 0=Mon .. 6=Sun
    enabled: bool = True
    snoozed_until: Optional[str] = None  # ISO datetime

    @staticmethod
    def create(
        time_iso: str,
        label: str = "",
        recurrence: Optional[str] = None,
        days: Optional[List[int]] = None,
    ) -> "Alarm":
        return Alarm(
            id=str(uuid.uuid4()),
            time_iso=time_iso,
            label=label,
            recurrence=recurrence,
            days=days,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "time_iso": self.time_iso,
            "label": self.label,
            "recurrence": self.recurrence,
            "days": self.days,
            "enabled": self.enabled,
            "snoozed_until": self.snoozed_until,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Alarm":
        return Alarm(
            id=d["id"],
            time_iso=d["time_iso"],
            label=d.get("label", ""),
            recurrence=d.get("recurrence"),
            days=d.get("days"),
            enabled=d.get("enabled", True),
            snoozed_until=d.get("snoozed_until"),
        )
