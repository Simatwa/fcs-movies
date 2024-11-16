"""Pydantic models"""

import typing as t
from pydantic import BaseModel, PositiveInt, HttpUrl


class V2SearchResultsItem(BaseModel):
    """Movie search results
    - `index` : Movie id in the database.
    - `title` : Movie title
    - `genre`: Movie genre
    - `category` : Hollywood|Bollywood
    - `year` : Release year
    - `distribution` : Distribution format.
    - `description` : Movie plot/about
    - `url` : Url pointing to the movie-page
    - `cover_photo` : Url to the movie album photo.
    """

    index: int
    title: str
    genre: t.Literal[
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
    category: t.Literal["Bollywood", "Hollywood", "All"]
    year: t.Optional[PositiveInt]
    distribution: t.Optional[str]
    description: t.Optional[str]
    url: HttpUrl
    cover_photo: HttpUrl


class V2SearchResults(BaseModel):
    """List of movies found"""

    movies: list[V2SearchResultsItem]
