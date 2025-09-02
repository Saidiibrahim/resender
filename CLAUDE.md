# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Modal-based Python project that sends scheduled emails via the Resend API. The project uses Modal's serverless platform to run cron jobs that send emails on a schedule.

## Key Commands

### Setup and Dependencies
```bash
# Preferred: using uv
uv pip install -e ".[dev]"

# Alternative: using pip
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Testing
```bash
pytest                    # Run all tests
pytest tests/test_*.py    # Run specific test file
```

### Code Quality
```bash
black .                   # Format code
ruff check .              # Lint code
ruff check --fix .        # Auto-fix linting issues
```

### Modal Operations
```bash
# Create required secret (if not exists)
modal secret create resend-secret RESEND_API_KEY=YOUR_KEY

# Run apps locally (test mode)
modal run src/resender/apps/weekly_email.py
modal run src/resender/apps/hello_world.py
modal run src/resender/apps/karpathy_daily_quote.py

# Deploy to Modal (production)
modal deploy src/resender/apps/weekly_email.py
modal deploy src/resender/apps/hello_world.py
modal deploy src/resender/apps/karpathy_daily_quote.py
```

## Architecture

### Directory Structure
```
src/resender/
├── apps/           # Modal applications with cron schedules
│   ├── weekly_email.py
│   ├── hello_world.py
│   └── karpathy_daily_quote.py
└── emails/         # Email utilities and sender functions
    └── sender.py   # Core email sending logic using Resend API
```

### Modal App Pattern
Each app in `src/resender/apps/` follows this pattern:
1. **Image definition**: Creates Modal container with dependencies (`resend` package)
2. **Secret reference**: References `resend-secret` containing `RESEND_API_KEY`
3. **Cron scheduling**: Uses `modal.Cron()` for scheduling (test vs production schedules)
4. **Function decoration**: `@app.function()` with image, schedule, and secrets
5. **Local entrypoint**: `@app.local_entrypoint()` for testing via `.remote()` calls

### Email Sending
The `resender.emails.sender` module provides:
- `send_email()`: Main function for sending emails via Resend API
- `get_resend_api_key()`: API key resolution from environment or explicit parameter
- Type hints and error handling for missing API keys

### Scheduling Strategy
Apps use two scheduling approaches:
- **Testing**: Frequent schedules (e.g., `*/10 * * * *` for every 10 minutes)
- **Production**: Actual schedules (e.g., `0 9 * * 1` for weekly Monday 9 AM)

Switch between schedules by commenting/uncommenting the appropriate `modal.Cron()` assignment.

## Development Notes

- Uses `src-layout` with `Image.add_local_python_source("resender")` for package imports
- All Modal functions require the custom image with `resend` dependency
- Secrets are attached at the function level, not app level
- Test functions locally using `.remote()` calls from `@app.local_entrypoint()`
- Line length is set to 100 characters for both Black and Ruff
- Python 3.11+ required