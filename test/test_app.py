def test_first_import():
    try:
        from app import create_app
        assert True
    except Exception as e:
        assert False,e
