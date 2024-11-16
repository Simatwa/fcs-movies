import pytest
from tests import client
from backend.v2 import models


@pytest.mark.parametrize(
    ["query", "genre", "category"],
    [
        ("Fast", "Action", "Hollywood"),
        ("Wrong", "Horror", "All"),
        ("Titan", "All", "All"),
    ],
)
def test_search(query, genre, category):
    resp = client.get(
        "/v2/search", params=dict(q=query, genre=genre, category=category)
    )
    jsonified_resp = resp.json()
    modelled_resp = models.V2SearchResults(**jsonified_resp)
    assert isinstance(modelled_resp, models.V2SearchResults)


def test_search_with_offset():
    limit = 10
    offset = 5
    query = "he"
    resp_without_offset = client.get(
        "/v2/search",
        params=dict(q=query, limit=limit),
    ).json()
    modelled_without = models.V2SearchResults(**resp_without_offset)
    resp_with_offset = client.get(
        "/v2/search", params=dict(q=query, limit=limit, offset=offset)
    ).json()
    modelled_with = models.V2SearchResults(**resp_with_offset)
    assert len(modelled_without.movies) > len(modelled_with.movies)
