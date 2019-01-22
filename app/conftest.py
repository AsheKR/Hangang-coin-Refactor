import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    모든 Test가 DB에 Access할 수 있게 해준다.

    """
    pass