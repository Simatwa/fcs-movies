import pytest
import fzmovies_api.models as fz_models
from backend import app
import backend.v1.models as v1_models
from tests import client


@pytest.mark.parametrize(
    ["query", "searchby", "category"],
    [
        ("Jason Statham", "Starcast", "Hollywood"),
        ("James Cameron", "Director", "All"),
        ("Wrong Turn", "Name", "Hollywood"),
    ],
)
def test_search(query, searchby, category):
    """Test movie search"""
    resp = client.post(
        "/api/v1/search", json=dict(q=query, searchby=searchby, category=category)
    )
    modelled_resp = fz_models.SearchResults(**resp.json())
    assert isinstance(modelled_resp, fz_models.SearchResults)


def test_search_with_offset():
    limit = 10
    offset = 5
    query = "wrong turn"
    resp_without_offset = client.post(
        "/api/v1/search",
        json=dict(q=query, limit=limit),
    ).json()
    modelled_without = fz_models.SearchResults(**resp_without_offset)
    resp_with_offset = client.post(
        "/api/v1/search", json=dict(q=query, limit=limit, offset=offset)
    ).json()
    modelled_with = fz_models.SearchResults(**resp_with_offset)
    assert len(modelled_without.movies) > len(modelled_with.movies)


def test_search_stream():
    resp = client.post(
        "/api/v1/search/stream",
        json=dict(q="hello"),
    )
    assert resp.is_success


def test_metadata():
    resp = client.post(
        "/api/v1/metadata",
        json=dict(
            movie_page_url="https://fzmovies.net/movie-Fast%20and%20Furious%207--hmp4.htm"
        ),
    )
    modelled_resp = fz_models.MovieFiles(**resp.json())
    assert isinstance(modelled_resp, fz_models.MovieFiles)


def test_download_link():
    resp = client.post(
        "/api/v1/metadata",
        json=dict(
            movie_page_url="https://fzmovies.net/movie-Fast%20and%20Furious%207--hmp4.htm"
        ),
    )
    metadata = fz_models.MovieFiles(**resp.json())
    resp1 = client.post(
        "/api/v1/download-link", json=dict(filename_url=str(metadata.files[0].url))
    )
    modelled_resp = v1_models.DownloadLink(**resp1.json())
    assert isinstance(modelled_resp, v1_models.DownloadLink)
