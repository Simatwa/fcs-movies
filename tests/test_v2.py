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
        "/api/v2/search", params=dict(q=query, genre=genre, category=category)
    )
    assert resp.is_success
    jsonified_resp = resp.json()
    models.ShallowSearchResults(**jsonified_resp)


def test_search_post():
    resp = client.post(
        "/api/v2/search",
        json={
            "category": "Hollywood",
            "distributions": ["BluRay"],
            "genres": ["Romance"],
            "limit": 10,
            "offset": 0,
            "query": "Love",
            "year": 2012,
            "year_offset": 0,
        },
    )
    assert resp.is_success
    models.V2SearchResults(**resp.json())


def test_search_specific_movie_id():
    resp = client.get("/api/v2/movie/1")
    assert resp.is_success
    models.V2SearchResultsItem(**resp.json())
