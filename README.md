# gym-tools

A Python package for collecting PureGym live attendance data via their unofficial API. Polls the number of people in a gym on a configurable interval and appends timestamped readings to a CSV file.

## Requirements

- Python 3.10+
- A PureGym account (email + numeric PIN)

## Installation

```bash
git clone <repo-url> gym-metrics
cd gym-metrics

python -m venv .venv
source .venv/bin/activate

pip install -e gymtools/
```

## Configuration

Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

```
# .env
PUREGYM_EMAIL=you@example.com
PUREGYM_PIN=12345678
```

Your PIN is the numeric code you use at the gym turnstile — not your website password.

| Variable | Required | Default | Description |
|---|---|---|---|
| `PUREGYM_EMAIL` | Yes | — | Account email address |
| `PUREGYM_PIN` | Yes | — | Numeric gym PIN |
| `PUREGYM_GYM_ID` | No | home gym | Integer gym ID (see below) |
| `DATA_FILE` | No | `gym_counts.csv` | Output CSV path |
| `POLL_INTERVAL_SECONDS` | No | `300` | Seconds between polls |

### Finding your gym ID

If `PUREGYM_GYM_ID` is not set, the collector defaults to the home gym on your account. To use a different gym, find its ID by inspecting the PureGym app traffic or checking community resources, then set it in `.env`.

## Usage

Load your env and activate the venv, then run the collector:

```bash
source .venv/bin/activate
set -a && source .env && set +a

gym-collect
```

The collector runs indefinitely, printing each reading to stdout and appending it to the CSV:

```
Using home gym ID: 42
2026-05-04T08:00:00+00:00  37 people
2026-05-04T08:05:00+00:00  41 people
...
```

The CSV is created with a header on first run and appended to on subsequent runs, so you can safely stop and restart without losing data:

```
timestamp,people_in_gym
2026-05-04T08:00:00+00:00,37
2026-05-04T08:05:00+00:00,41
```

## Project structure

```
gymtools/
  gymtools/
    puregym_api.py   # PureGymClient — auth and API calls
    collect.py       # polling loop and CSV writer
  pyproject.toml
.env.example         # env var template (copy to .env)
.gitignore           # excludes .env, .venv, and gym_counts.csv
```

## Notes

- This uses PureGym's **unofficial** mobile API (reverse-engineered). It may break if PureGym changes their backend.
- The API uses v2 endpoints (`capi.puregym.com/api/v2`). The v1 endpoints were deprecated in late 2025.
- Tokens are refreshed automatically on 401 responses — no manual re-auth needed for long-running sessions.
- `.env` is gitignored. Never commit your credentials.

## Disclaimer
You use this tool **at your own risk**, accepting that your account may be banned as a result.
