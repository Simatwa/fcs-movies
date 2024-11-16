from tests import client


def test_index():
    resp = client.get("/")
    assert resp.is_success
