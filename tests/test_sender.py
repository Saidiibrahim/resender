def test_import_sender():
    from resender.emails.sender import send_email, get_resend_api_key

    assert callable(send_email)
    assert callable(get_resend_api_key)
