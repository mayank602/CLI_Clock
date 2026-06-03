from __future__ import annotations
import click
from .scheduler import AlarmManager
from .models import Alarm
from datetime import datetime


@click.group()
def cli():
    """Alarm Clock CLI"""


@cli.command()
@click.argument("time")
@click.option("--label", "label", default="", help="Label for the alarm")
@click.option("--daily", "daily", is_flag=True, help="Make this alarm recur daily")
@click.option("--weekly", "weekly", help="Comma separated weekdays 0=Mon..6=Sun")
def add(time, label, daily, weekly):
    """Add an alarm. TIME can be HH:MM or ISO date/time."""
    mgr = AlarmManager()
    recurrence = None
    days = None
    if daily:
        recurrence = "daily"
    if weekly:
        recurrence = "weekly"
        days = [int(x) for x in weekly.split(",") if x.strip().isdigit()]
    alarm = Alarm.create(time_iso=time, label=label, recurrence=recurrence, days=days)
    mgr.add_alarm(alarm)
    click.echo(
        f"Added alarm {alarm.id} -> {alarm.time_iso} {alarm.recurrence or 'once'}"
    )


@cli.command(name="list")
def _list():
    """List alarms"""
    mgr = AlarmManager()
    for a in mgr.list_alarms():
        click.echo(
            f"{a.id} | {a.time_iso} | {a.label} | {a.recurrence or 'once'} | enabled={a.enabled}"
        )


@cli.command()
@click.argument("alarm_id")
def remove(alarm_id):
    """Remove an alarm by id"""
    mgr = AlarmManager()
    ok = mgr.remove_alarm(alarm_id)
    if ok:
        click.echo("Removed")
    else:
        click.echo("Not found")


@cli.command()
@click.option("--interval", default=1.0, help="Poll interval seconds")
def run(interval):
    """Run the alarm manager (blocking)"""
    mgr = AlarmManager()
    click.echo("Starting alarm manager (Ctrl+C to stop)")
    mgr.run(poll_interval=interval)


@cli.command()
@click.argument("alarm_id")
@click.option("--minutes", default=5, help="Minutes to snooze")
def snooze(alarm_id, minutes):
    """Snooze an alarm by id for N minutes"""
    mgr = AlarmManager()
    ok = mgr.snooze(alarm_id, minutes)
    if ok:
        click.echo(f"Snoozed {alarm_id} for {minutes} minutes")
    else:
        click.echo("Not found")


@cli.command(name="test-sound")
def test_sound():
    """Play the bundled alarm sound (or fallback)"""
    mgr = AlarmManager()
    from .audio import play_alarm

    play_alarm(mgr.asset_wav)
    click.echo("Played alarm sound")
