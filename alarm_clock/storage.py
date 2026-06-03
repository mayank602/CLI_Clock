from __future__ import annotations
import json
from pathlib import Path
from typing import List
from .models import Alarm


class Storage:
    def __init__(self, data_dir: Path | str = None):
        if data_dir is None:
            home = Path.home()
            data_dir = home / ".alarm_clock"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.data_dir / "alarms.json"

    def load(self) -> List[Alarm]:
        if not self.file.exists():
            return []
        try:
            with self.file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return []
        return [Alarm.from_dict(d) for d in data]

    def save(self, alarms: List[Alarm]) -> None:
        tmp = self.file.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump([a.to_dict() for a in alarms], f, indent=2)
        tmp.replace(self.file)
