import os
from typing import Optional, Sequence, Any


def get_resend_api_key(explicit_api_key: Optional[str] = None) -> str:
    """Return a Resend API key from an explicit value or the RESEND_API_KEY env var.

    Raises RuntimeError if no key is available.
    """
    if explicit_api_key and explicit_api_key.strip():
        return explicit_api_key

    api_key = os.environ.get("RESEND_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "RESEND_API_KEY is not set. Provide it via environment or a Modal secret."
        )
    return api_key


def send_email(
    *,
    sender: str,
    recipients: Sequence[str],
    subject: str,
    html: str,
    text: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Any:
    """Send an email using Resend.

    Parameters are plain strings/collections for easy reuse across the app.
    """
    # Import inside the function so it resolves within the Modal container image
    import resend  # type: ignore

    resolved_api_key = get_resend_api_key(api_key)
    resend.api_key = resolved_api_key

    params: "resend.Emails.SendParams" = {
        "from": sender,
        "to": list(recipients),
        "subject": subject,
        "html": html,
    }
    if text is not None and text.strip():
        params["text"] = text
    return resend.Emails.send(params)
