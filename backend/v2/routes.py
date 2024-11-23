"""V2 Routes"""

import typing as t
from fastapi import APIRouter, HTTPException, status, Query, Path
import backend.v2.models as models
from backend.database import Movie, Category, Genre
import backend.utils as utils
from backend.config import config
from backend.database import session
from sqlalchemy import text

router = APIRouter()

total_movies = session.execute(text("SELECT COUNT(id) FROM movie")).first()[0]


@router.get("/search", name="Search movie")
@utils.router_exception_handler
async def search_movie(
    q: str = Query(description="Movie title"),
    limit: t.Optional[int] = Query(
        config.search_limit_per_query, description="Total movie titles not to exceed"
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
def get_specific_movie_info(
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
