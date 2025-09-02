from datetime import datetime

import modal
from resender.emails.sender import send_email


email_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("resend")
    .add_local_python_source("resender")
)

app = modal.App("karpathy-daily-quote")
resend_secret = modal.Secret.from_name("resend-secret")


# Daily at 9 AM Adelaide time
daily_schedule = modal.Cron("0 9 * * *", timezone="Australia/Adelaide")


def _quote_html(date_str: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Karpathy Quote</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center;">
            <h1 style="margin: 0; font-size: 24px; font-weight: 600;">Daily Wisdom</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 14px;">Insights for continuous learning</p>
        </div>
        
        <div style="background: #f8f9fa; border-left: 4px solid #667eea; padding: 25px; border-radius: 8px; margin-bottom: 25px;">
            <h2 style="margin: 0 0 20px 0; color: #2c3e50; font-size: 20px;">How to become expert at thing:</h2>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #667eea;">1</strong> 
                <span style="margin-left: 10px;">iteratively take on concrete projects and accomplish them depth wise, learning \"on demand\" (ie don't learn bottom up breadth wise)</span>
            </div>
            
            <div style="margin-bottom: 15px;">
                <strong style="color: #667eea;">2</strong> 
                <span style="margin-left: 10px;">teach/summarize everything you learn in your own words</span>
            </div>
            
            <div>
                <strong style="color: #667eea;">3</strong> 
                <span style="margin-left: 10px;">only compare yourself to younger you, never to others</span>
            </div>
        </div>
        
        <div style="text-align: center; color: #666; font-size: 14px; border-top: 1px solid #eee; padding-top: 20px;">
            <p style="margin: 0;">— Andrej Karpathy (@karpathy)</p>
            <p style="margin: 5px 0 0 0; font-size: 12px;">Sent on {date_str}</p>
        </div>
        
    </body>
    </html>
    """


def _quote_text() -> str:
    return (
        "How to become expert at thing:\n\n"
        '1. iteratively take on concrete projects and accomplish them depth wise, learning "on demand" (ie don\'t learn bottom up breadth wise)\n\n'
        "2. teach/summarize everything you learn in your own words\n\n"
        "3. only compare yourself to younger you, never to others\n\n"
        "— Andrej Karpathy (@karpathy)"
    )


@app.function(
    image=email_image,
    schedule=daily_schedule,
    secrets=[resend_secret],
)
def send_karpathy_daily_quote():
    subject = "Daily Wisdom: How to Become an Expert"
    date_str = datetime.now().strftime("%B %d, %Y")
    html = _quote_html(date_str)
    text = _quote_text()

    send_email(
        sender="onboarding@resend.dev",
        recipients=["ibrahim.aka.ajax@gmail.com"],
        subject=subject,
        html=html,
        text=text,
    )


@app.local_entrypoint()
def main():
    # Secrets are attached to the function; just invoke it remotely.
    send_karpathy_daily_quote.remote()
