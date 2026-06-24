---
title: Python Dates
summary: Working with dates and times using the datetime module.
related: python-strings, python-string-formatting, python-modules
---

Python's date and time tools live in the `datetime` module. The four main classes:

- `date` — a calendar date (year, month, day)
- `time` — a wall-clock time (hours, minutes, seconds, microseconds)
- `datetime` — both combined
- `timedelta` — a duration

```python
from datetime import date, datetime, timedelta

today = date.today()             # 2026-06-07
now   = datetime.now()           # 2026-06-07 14:32:11.123456
yesterday = today - timedelta(days=1)
```

**Formatting and parsing strings**:

```python
now.strftime("%Y-%m-%d %H:%M")   # "2026-06-07 14:32"
datetime.strptime("2026-06-07", "%Y-%m-%d")
```

Common format codes: `%Y` (year), `%m` (month), `%d` (day), `%H` (24-hour), `%M` (minute), `%S` (second).

**Arithmetic with timedeltas**:

```python
in_a_week = now + timedelta(days=7)
delta = in_a_week - now          # timedelta(days=7)
delta.days                       # 7
delta.total_seconds()            # 604800.0
```

- Always store timestamps in UTC. Convert to local time only at display.
- For timezone-aware datetimes use `datetime.now(timezone.utc)` and the `zoneinfo` module (3.9+).
- For ISO 8601 strings, `datetime.fromisoformat("2026-06-07T14:32")` is the easiest parser.

---

<div class="callout">
<p class="callout-yes"><strong>✓ Use it when</strong> — `datetime` for any timestamp; `datetime.now(timezone.utc)` to record events.</p>
<p class="callout-no"><strong>✗ Skip it when</strong> — Naive datetimes for anything that crosses servers, timezones, or daylight-saving boundaries. The bugs only appear in production.</p>
</div>

