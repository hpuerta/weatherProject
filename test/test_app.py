def test_first_import():
    try:
        from app import create_app
        assert True
    except Exception as e:
        assert False,e

from app import create_app
def test_get_enviroment_variables_as_config():
    try:
        app = create_app()
        assert app.config['TEST_VAR']=="my_value"
    except Exception as e:
        assert False,e