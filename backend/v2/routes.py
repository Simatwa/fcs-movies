"""V2 Routes"""

import typing as t
from fastapi import APIRouter, HTTPException, status, Query, Path
import backend.v2.models as models
from backend.database import Movie, NormalDownloadLink, BestDownloadLink
from backend.database import session
import backend.utils as utils
from backend.config import config, logger
from sqlalchemy import text
import fzmovies_api.models as fz_models
from fzmovies_api import Navigate, DownloadLinks, Download
from backend.v1 import models as v1_models
from datetime import timedelta
from sqlalchemy.exc import OperationalError

router = APIRouter()

total_movies = session.execute(text("SELECT COUNT(id) FROM movie")).first()[0]

quality_model_map = {
    "normal": NormalDownloadLink,
    "best": BestDownloadLink,
}


def clear_expired_download_links():
    time = utils.utcnow().replace(tzinfo=None) - timedelta(
        hours=config.download_link_cache_duration_in_hours
    )
    for table in ["normal_download_link", "best_download_link"]:
        logger.info(f"Clearing expired download links in {table} table")
        try:
            session.execute(text(f"DELETE FROM {table} WHERE updated_on < '{time}'"))
            session.commit()
        except OperationalError:
            # Tables are missing which is still okay
            pass


router.add_event_handler("startup", clear_expired_download_links)


@router.get("/search", name="Search movie")
@utils.router_exception_handler
async def search_movie(
    q: str = Query(description="Movie title"),
    limit: t.Optional[int] = Query(
        config.search_limit_per_query,
        description="Total movie titles not to exceed",
        gt=0,
        le=config.search_limit_per_query,
    ),
    offset: t.Optional[int] = Query(0, description="Search results offset"),
    year_offset: t.Optional[int] = Query(0, description="Movie realease year offset"),
) -> models.ShallowSearchResults:
    """Search movies from cache and return shallow results"""
    movies = (
        session.query(Movie)
        .filter(Movie.title.like(f"%{q}%"), Movie.year > year_offset)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return models.ShallowSearchResults(
        query=q, results=[dict(id=movie.id, title=str(movie)) for movie in movies]
    )


@router.post("/search", name="Search movies deeply")
@utils.router_exception_handler
async def search_movies_by_post(search: models.SearchByPost) -> models.V2SearchResults:
    """Search movies from cache and return whole movie metadata"""
    filters = [Movie.year >= search.year_offset]
    if search.query:
        filters.append(Movie.title.like(f"%{search.query}%"))
    """
    if search.category:
        filters.append(
            Movie.category.name == search.category
            )
    if search.genres:
        filters.append(
            Movie.genres.name.in_(search.genres)
            )
    """
    if search.description:
        filters.append(Movie.description.like(f"%{search.description}%"))
    if search.distributions:
        filters.append(Movie.distribution.in_(search.distributions))
    if search.year:
        filters.append(Movie.year == search.year)

    movies = (
        session.query(Movie)
        .filter(*filters)
        .offset(search.offset)
        .limit(search.limit)
        .all()
    )
    return models.V2SearchResults(
        query=search.query, movies=[movie.model_dump() for movie in movies]
    )


@router.get("/movie/{id}")
@utils.router_exception_handler
async def get_specific_movie_info(
    id: int = Path(description="Movie id", ge=1, le=total_movies)
) -> models.V2SearchResultsItem:
    """Get metadata for a particular movie"""
    movie = session.get(Movie, id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There's no movie with id '{id}.'",
        )
    return models.V2SearchResultsItem(**movie.model_dump())


@router.get("/metadata/{id}")
@utils.router_exception_handler
async def get_movie_metadata_2(
    id: int = Path(description="Movie id", ge=1, le=total_movies)
) -> v1_models.MovieFiles:
    """Get metadata for a particular movie"""
    movie = session.get(Movie, id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There's no movie with id '{id}.'",
        )
    nav = Navigate(
        fz_models.MovieInSearch(
            url=movie.url,
            title="",
            year=1,
            distribution="",
            about="",
            cover_photo="https://somelink-here",
        )
    )
    return nav.results


@router.get("/download-link/{id}", name="Download link metadata")
@utils.router_exception_handler
async def download_link_by_id(
    id: int = Path(description="Movie id", ge=1, le=total_movies),
    quality: t.Literal["normal", "best"] = Query(
        "best", description="Movie file quality"
    ),
) -> v1_models.DownloadLink:
    """Get link to the desired movie-file"""
    movie = session.get(Movie, id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There's no movie with id '{id}.'",
        )

    download_link_model: BestDownloadLink = quality_model_map[quality]
    cached_results: BestDownloadLink = session.get(download_link_model, id)
    if cached_results and (
        utils.utcnow().replace(tzinfo=None) - cached_results.updated_on
    ) < timedelta(hours=config.download_link_cache_duration_in_hours):
        return v1_models.DownloadLink(**cached_results.model_dump())

    nav = Navigate(
        fz_models.MovieInSearch(
            url=movie.url,
            title="",
            year=1,
            distribution="",
            about="",
            cover_photo="https://somelink-here",
        )
    )
    target_file = nav.results.files[0 if quality == "normal" else 1]
    download_movie = DownloadLinks(
        fz_models.FileMetadata(
            title="some-movie-title",
            url=target_file.url,
            size="",
            hits=0,
            mediainfo="https://yet-another-link",
        )
    ).results
    filename = download_movie.filename
    target_link = download_movie.links[0]
    movie_file = Download(target_link).last_url
    if cached_results:
        # Update the url and filename
        cached_results.url = movie_file
        cached_results.filename = filename
    else:
        # Insert new entry
        session.add(download_link_model(id=id, filename=filename, url=movie_file))
    session.commit()
    return v1_models.DownloadLink(filename=filename, url=movie_file)
