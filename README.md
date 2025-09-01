## Resender

Modal cron jobs that send emails via Resend.

### Layout

```
src/resender/apps/
  hello_world.py
  weekly_email.py
tests/
  test_smoke.py
```

### Setup

Using uv (recommended) or pip.

```bash
# uv
uv pip install -e ".[dev]"

# pip
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Modal secret

Create a secret named `resend-api-key` that holds `RESEND_API_KEY`.

```bash
modal secret create resend-api-key RESEND_API_KEY=YOUR_KEY
```

### Run locally

```bash
modal run src/resender/apps/weekly_email.py
```

### Deploy the schedule

```bash
modal deploy src/resender/apps/weekly_email.py
```

Switch from the every-10-min schedule to weekly by toggling the cron in `weekly_email.py`.
