"""V2 Routes"""

import typing as t
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
import backend.v2.models as models
import backend.database as db
import backend.utils as utils
from backend.config import config

router = APIRouter()


@router.get("/search", name="Search movie")
@utils.router_exception_handler
async def search_movie(
    q: t.Optional[str] = None,
    genre: t.Optional[
        t.Literal[
            "Action",
            "Adventure",
            "Animation",
            "Biography",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Family",
            "Fantasy",
            "Film-Noir",
            "History",
            "Horror",
            "Music",
            "Musical",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Sport",
            "Thriller",
            "War",
            "Western",
            "All",
        ]
    ] = "All",
    category: t.Optional[t.Literal["Bollywood", "Hollywood", "All"]] = "All",
    year: t.Optional[int] = 0,
    description: t.Optional[str] = None,
    distribution: t.Optional[str] = "All",
    limit: t.Optional[int] = config.search_limit_per_query,
    offset: t.Optional[int] = 0,
    index: t.Optional[int] = 0,
) -> models.V2SearchResults:
    """Search movies from cache
    - `q` : Movie title.
    - `genre` : Movie genre.
    - `category`: Movie category.
    - `year` : Movie release year.
    - `description` : Movie about.
    - `distribution` : Distribution format.
    - `limit` : Search limit.
    - `offset` : Results offset.
    - `index` : Movie index offset.
    """
    search_filters = []

    if q:
        search_filters.append(db.Movies.title.like(f"%{q}%"))
    if genre != "All":
        search_filters.append(db.Movies.genre.like(f"%{genre}%"))
    if category != "All":
        search_filters.append(db.Movies.category.like(f"%{category}%"))
    if year:
        search_filters.append(db.Movies.year == year)
    if description:
        search_filters.append(db.Movies.description.like(f"%{description}%"))
    if distribution != "All":
        search_filters.append(db.Movies.distribution.like(f"%{distribution}%"))
    if index:
        search_filters.append(db.Movies.index > index)

    results = db.session.query(db.Movies).filter(*search_filters).limit(limit).all()
    sorted_results = [jsonable_encoder(result) for result in results]
    if len(sorted_results) > offset:
        sorted_results = sorted_results[offset:]
    return models.V2SearchResults(movies=sorted_results)
