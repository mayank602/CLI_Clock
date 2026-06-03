from datetime import datetime, timedelta
from alarm_clock.scheduler import AlarmManager
from alarm_clock.models import Alarm


def add_alarm_for_next_minute():
    t = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
    mgr = AlarmManager()
    alarm = Alarm.create(time_iso=t, label="SmokeTest")
    mgr.add_alarm(alarm)
    print("Added alarm:", alarm.id, t)


if __name__ == "__main__":
    add_alarm_for_next_minute()
