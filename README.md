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

Use an existing secret named `resend-secret` that contains the key `RESEND_API_KEY` (as in the Modal dashboard screenshot). If you need to create it from the CLI:

```bash
modal secret create resend-secret RESEND_API_KEY=YOUR_KEY
```

### Run locally

Src-layout note: the Modal images now include the local `resender` package via `Image.add_local_python_source("resender")`, so imports work when running remotely and you do not need to set `PYTHONPATH`.

```bash
modal run src/resender/apps/weekly_email.py
```

### Deploy the schedule

```bash
modal deploy src/resender/apps/weekly_email.py
```

Switch from the every-10-min schedule to weekly by toggling the cron in `weekly_email.py`.
