import pytest
from modules.tumblrEmail import EmailChecker


@pytest.mark.parametrize("id", ["justinmat1994@gmail.com", "justinmat199@gmail.com"])
def test_id_checker(id):
    obj = EmailChecker()
    response = obj.checker(id)

    assert type(response['profileExists']) == bool

    if type(response['profileExists']) is True:
        assert isinstance(response['profile'], str)
