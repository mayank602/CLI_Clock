# Alarm Clock (CLI)

Simple cross-platform Python CLI alarm clock.

Usage examples:

Install dependencies (optional):

```bash
python -m pip install -r requirements.txt
```

Add an alarm (today at 07:30):

```bash
python main.py add 07:30 --label "Wake up"
```

Add a daily alarm:

```bash
python main.py add 07:30 --daily
```

Run the alarm manager (blocking):

```bash
python main.py run
```

List alarms:

```bash
python main.py list
```

Test sound:

```bash
python main.py test-sound
```
