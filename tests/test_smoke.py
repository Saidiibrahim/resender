def test_import_weekly_email():
    import resender.apps.weekly_email as mod

    assert hasattr(mod, "app")

