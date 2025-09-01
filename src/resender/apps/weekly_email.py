import os
import modal
from resender.emails.sender import send_email

# Define a custom image that installs the Resend Python SDK
# The default Modal image is Debian with Python; we add our dependency with pip_install.
email_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("resend")
    .add_local_python_source("resender")
)

# Create the Modal application
app = modal.App("weekly-email-app")

# Reference a secret containing your RESEND_API_KEY (create this in the Modal dashboard or CLI)
resend_secret = modal.Secret.from_name("resend-secret")

# --- Scheduling ---
# For testing, schedule the function every 10 minutes. Once testing is complete,
# you can comment out the 10-minute cron schedule and uncomment the weekly cron
# schedule below.

# Runs every 10 minutes in the Australia/Adelaide time zone.
current_schedule = modal.Cron("*/10 * * * *", timezone="Australia/Adelaide")

# Weekly schedule (commented out): runs every Monday at 9 AM Adelaide time.
# weekly_schedule = modal.Cron("0 9 * * 1", timezone="Australia/Adelaide")

@app.function(
    image=email_image,
    schedule=current_schedule,
    secrets=[resend_secret],
)
def send_weekly_email():
    """Send a weekly email using Resend."""
    send_email(
        sender="Acme <onboarding@resend.dev>",
        recipients=["ibrahim.aka.ajax@gmail.com"],
        subject="Weekly digest",
        html="""
            <h1>Weekly Update</h1>
            <p>Hello! This is your weekly email sent via Modal and Resend.</p>
            <p>This is a test email.</p>
        """,
    )

@app.local_entrypoint()
def main():
    """Test the email-sending function locally."""
    # Secrets are attached to the function; just invoke it remotely.
    send_weekly_email.remote()
