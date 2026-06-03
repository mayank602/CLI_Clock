from __future__ import annotations
from datetime import datetime, time, timedelta
import time as time_module
from typing import List, Optional
from .models import Alarm
from .storage import Storage
from .audio import play_alarm, ensure_alarm_wav
from pathlib import Path


class AlarmManager:
    def __init__(self, storage: Optional[Storage] = None):
        self.storage = storage or Storage()
        self.alarms: List[Alarm] = self.storage.load()
        self.asset_wav = Path(self.storage.data_dir) / "alarm.wav"
        ensure_alarm_wav(self.asset_wav)

    def add_alarm(self, alarm: Alarm) -> None:
        self.alarms.append(alarm)
        self.storage.save(self.alarms)

    def remove_alarm(self, alarm_id: str) -> bool:
        before = len(self.alarms)
        self.alarms = [a for a in self.alarms if a.id != alarm_id]
        if len(self.alarms) != before:
            self.storage.save(self.alarms)
            return True
        return False

    def list_alarms(self) -> List[Alarm]:
        return self.alarms

    def snooze(self, alarm_id: str, minutes: int = 5) -> bool:
        for a in self.alarms:
            if a.id == alarm_id:
                dt = datetime.now() + timedelta(minutes=minutes)
                a.snoozed_until = dt.isoformat()
                self.storage.save(self.alarms)
                return True
        return False

    def _alarm_next_run(self, alarm: Alarm, now: datetime) -> Optional[datetime]:
        # If snoozed
        if alarm.snoozed_until:
            try:
                dt = datetime.fromisoformat(alarm.snoozed_until)
                if dt > now:
                    return dt
            except Exception:
                pass

        # Parse alarm.time_iso which may be date+time or time-only (HH:MM)
        try:
            if "T" in alarm.time_iso or " " in alarm.time_iso or "-" in alarm.time_iso:
                # date or datetime
                dt = datetime.fromisoformat(alarm.time_iso)
                if dt >= now:
                    return dt
                # if past and recurring, compute next
            else:
                hh, mm = map(int, alarm.time_iso.split(":"))
                candidate = datetime.combine(now.date(), time(hh, mm))
                if candidate >= now:
                    return candidate
                # otherwise, tomorrow or next recurrence
        except Exception:
            return None

        if alarm.recurrence == "daily":
            # next day at the same time
            try:
                hh, mm = map(int, alarm.time_iso.split(":"))
                return datetime.combine(now.date() + timedelta(days=1), time(hh, mm))
            except Exception:
                return None

        if alarm.recurrence == "weekly" and alarm.days:
            # find next weekday in alarm.days (0=Mon)
            try:
                hh, mm = map(int, alarm.time_iso.split(":"))
            except Exception:
                return None
            for d in range(1, 8):
                candidate_date = now.date() + timedelta(days=d)
                if candidate_date.weekday() in alarm.days:
                    return datetime.combine(candidate_date, time(hh, mm))

        # one-time in past
        return None

    def run(self, poll_interval: float = 1.0):
        try:
            while True:
                now = datetime.now()
                for alarm in list(self.alarms):
                    if not alarm.enabled:
                        continue
                    next_run = self._alarm_next_run(alarm, now)
                    if next_run and next_run <= now:
                        print(
                            f"Alarm triggered: {alarm.id} {alarm.label} at {now.isoformat()}"
                        )
                        play_alarm(self.asset_wav)
                        # clear snooze
                        alarm.snoozed_until = None
                        # if recurrence not set, disable the alarm
                        if not alarm.recurrence:
                            alarm.enabled = False
                        self.storage.save(self.alarms)
                time_module.sleep(poll_interval)
        except KeyboardInterrupt:
            print("\nAlarm manager stopped by user")
