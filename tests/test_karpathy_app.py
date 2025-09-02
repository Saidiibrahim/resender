def test_import_karpathy_app():
    import resender.apps.karpathy_daily_quote as appmod

    assert hasattr(appmod, "app")
    assert hasattr(appmod, "send_karpathy_daily_quote")
