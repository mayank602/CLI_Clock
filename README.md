# CLI Alarm Clock

A small cross-platform command-line alarm clock written in Python. It supports multiple alarms, daily and weekly recurrences, snooze, local JSON persistence, and plays a bundled WAV alarm sound (with fallbacks to platform audio or terminal bell).

This project is intentionally lightweight and dependency-minimal so it can run easily on Windows, macOS, and Linux.

**Status:** Working prototype — currently a foreground process. Alarms are stored locally in a JSON file under your home directory.

**Repository:** https://github.com/mayank602/CLI_Clock

---

## Features

- Add, list, and remove alarms from the CLI
- Support for one-time alarms (HH:MM or ISO datetime)
- Recurring alarms: daily and weekly (specify weekdays)
- Snooze an alarm for N minutes
- Local JSON persistence (`~/.alarm_clock/alarms.json`)
- Bundled WAV alarm sound (auto-generated if missing) with playback via `simpleaudio` (if available) or `winsound` (Windows) or terminal bell fallback
- Small smoke test helper to add a +1 minute alarm

---

## Project Structure

- `alarm_clock/` — package source
  - `__init__.py` — package init
  - `models.py` — `Alarm` dataclass and serialization
  - `storage.py` — JSON load/save (atomic write)
  - `audio.py` — generate/play bundled WAV with fallbacks
  - `scheduler.py` — `AlarmManager` run loop, next-run logic, snooze handling
  - `cli.py` — `click` CLI commands: `add`, `list`, `remove`, `run`, `snooze`, `test-sound`
- `main.py` — thin CLI entrypoint
- `scripts/smoke_add.py` — helper to add a smoke alarm for +1 minute
- `requirements.txt` — optional runtime dependencies
- `README.md` — this file

---

## Installation

Requires Python 3.10+.

Clone the repo and (optionally) create a virtual environment:

```bash
git clone https://github.com/mayank602/CLI_Clock.git
cd CLI_Clock
python -m venv .venv
# Activate the venv (Windows):
# .venv\Scripts\activate
# (macOS/Linux): source .venv/bin/activate
```

Optional: install `simpleaudio` for better playback (the project works without it):

```bash
python -m pip install -r requirements.txt
```

---

## Usage

Run the CLI via `python main.py <command>` or `python -m alarm_clock <command>`.

Add a one-time alarm for today (or next occurrence) at 07:30:

```bash
python main.py add 07:30 --label "Wake up"
```

Add a daily recurring alarm at 07:30:

```bash
python main.py add 07:30 --daily --label "Daily Wake"
```

Add a weekly alarm on Mondays (0) and Fridays (4) at 08:00:

```bash
python main.py add 08:00 --weekly 0,4 --label "Mon/Fri Meeting"
```

List alarms:

```bash
python main.py list
```

Remove an alarm by id:

```bash
python main.py remove <alarm_id>
```

Start the alarm manager (blocking). Keep this process running for alarms to trigger:

```bash
python main.py run
```

Snooze an alarm:

```bash
python main.py snooze <alarm_id> --minutes 10
```

Test the bundled alarm sound:

```bash
python main.py test-sound
```

Quick smoke test (adds an alarm one minute in the future):

```bash
python scripts/smoke_add.py
python main.py run
```

---

## How it works (runtime)

1. Alarms are created using the `add` command and saved to a JSON file in your home directory (`~/.alarm_clock/alarms.json`).
2. `python main.py run` starts a polling loop that checks alarms every second (configurable). When an alarm's next-run time is reached the app plays the bundled sound and updates alarm state.
3. One-time alarms are disabled after firing. Recurring alarms compute the next run based on `daily` or `weekly` settings.
4. Snooze sets a temporary `snoozed_until` timestamp; the scheduler honors snooze before computing recurrence.

---

## Limitations & Notes

- The app runs in the foreground: if the process exits, alarms will not trigger. For persistent background behavior, run the script as a system service (systemd, Task Scheduler, etc.).
- Time handling uses the system's local timezone and naive datetimes; no timezone conversions are performed.
- Audio playback depends on platform and available Python packages. If playback fails, the program will emit a terminal bell as a fallback.
- The polling scheduler is sufficient for minute/second-level alarms, but not for high-precision timing.

---

## Development & Testing

- Add unit tests for parsing and scheduling logic (not included yet). Recommended tools: `pytest`, `freezegun` for time-freezing.
- To run the quick manual smoke test:

```bash
python scripts/smoke_add.py
python main.py run
```

---

## Contributing

Contributions welcome. Suggested ways to help:

- Add unit tests for `scheduler._alarm_next_run` and recurrence logic
- Improve CLI UX and error messages
- Add system-service installation scripts or packaging (`pyproject.toml` + console scripts)

---

## License

This project is provided as-is. Add a license file if you plan to open-source it publicly.
