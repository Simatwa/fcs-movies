"""v1 Routes
"""

import typing as t
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
import backend.v1.models as models
import backend.v1.utils as utils
from fzmovies_api import Search, Navigate, DownloadLinks, Download
import fzmovies_api.models as fz_models
from json import dumps

router = APIRouter()


@router.post("/search", name="Search")
@utils.router_exception_handler
async def search(search: models.Search) -> fz_models.SearchResults:
    """Search movies using filters"""
    searchq = Search(query=search.q, searchby=search.searchby, category=search.category)
    resp = searchq.get_all_results(limit=search.limit)
    print(search.offset)
    if resp.movies and len(resp.movies) > search.offset:
        current_movies = resp.movies
        resp.movies = current_movies[search.offset :]
    return resp


@router.post("/search/stream", name="Search stream")
@utils.router_exception_handler
async def search_stream(
    search: models.SearchStream,
) -> t.Annotated[t.Generator[fz_models.SearchResults, None, None], StreamingResponse]:
    """Search movies using filters and stream results"""
    searchq = Search(query=search.q, searchby=search.searchby, category=search.category)

    def generate_streaming_response():
        for results in searchq.get_all_results(stream=True, limit=search.limit):
            yield dumps(jsonable_encoder(results)) + "\n"

    return StreamingResponse(
        generate_streaming_response(), media_type="application/json"
    )


@router.post("/metadata", name="Movie metadata")
@utils.router_exception_handler
async def movie_metadata(target: models.TargetMovie) -> fz_models.MovieFiles:
    """Get metadata for a particular movie"""
    nav = Navigate(
        fz_models.MovieInSearch(
            url=target.movie_page_url,
            title="",
            year=1,
            distribution="",
            about="",
            cover_photo="https://somelink-here",
        )
    )
    return nav.results


@router.post("/download-link", name="Download link metadata")
@utils.router_exception_handler
async def download_link(target: models.TargetFilename) -> t.Union[models.DownloadLink]:
    """Get link to the desire movie-file"""
    download_movie = DownloadLinks(
        fz_models.FileMetadata(
            title="some-movie-title",
            url=target.filename_url,
            size="",
            hits=0,
            mediainfo="https://yet-another-link",
        )
    ).results
    filename = download_movie.filename
    target_link = download_movie.links[0]
    movie_file = Download(target_link).last_url
    return models.DownloadLink(filename=filename, url=movie_file)
