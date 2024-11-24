"""Pydantic models"""

import typing as t
from pydantic import BaseModel, PositiveInt, HttpUrl, Field, field_validator
from backend.config import config


class ShallowSearchResults(BaseModel):
    """Search results containing movie `titles` and `id` only"""

    class MovieTitleId(BaseModel):
        id: int = Field(description="Movie identity number")
        title: str = Field(description="Movie title name")

        model_config = {
            "json_schema_extra": {
                "example": {"id": 51, "title": "This Means War (2012)"},
            }
        }

    query: str = Field(description="Search query value")
    results: list[MovieTitleId] = Field(description="Movie `title` and `id`")

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "war",
                "results": [
                    {"id": 51, "title": "This Means War (2012)"},
                    {"id": 92, "title": "Warm Bodies (2013)"},
                    {"id": 147, "title": "That Awkward Moment (2014)"},
                    {"id": 289, "title": "My Awkward Sexual Adventure (2013)"},
                    {"id": 375, "title": "Edward Scissorhands (1989)"},
                ],
            }
        }
    }


class SearchByPost(BaseModel):
    query: t.Optional[str] = Field(None, description="Movie title name")
    genres: t.Optional[
        list[
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
            ]
        ]
    ] = Field(
        None,
        description="Movie genre names.",
    )
    category: t.Optional[t.Literal["Bollywood", "Hollywood"]] = Field(
        "Hollywood",
        description="Movie category name as in Bollywood etc.",
    )
    year: t.Optional[PositiveInt] = Field(
        None, description="Movie official release year"
    )
    distributions: t.Optional[
        list[
            t.Literal[
                "BluRay",
                "WEB-DL",
                "HDRip",
                "DVDR",
                "WEBRip",
                "BRRip",
                "DVDRip",
                "CAMRip",
                "HDTV",
                "BDRip",
                "Unknown",
                "DVDRip720p",
                "DVDSCR",
                "PDVDRip",
                "TS",
                "VODRip",
                "R5",
                "All",
            ]
        ]
    ] = Field(None, description="Movie ditribution formats")
    description: t.Optional[str] = Field(None, description="Movie about a.k.a plot")
    limit: t.Optional[int] = Field(
        config.search_limit_per_query,
        description="Total number of movies not to exceed",
    )
    offset: t.Optional[int] = Field(0, description="Search results offset")
    year_offset: t.Optional[int] = Field(0, description="Movie release year offset")

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "Love",
                "genres": ["Romance"],
                "category": "Hollywood",
                "year": 2012,
                "distributions": ["BluRay"],
                "description": None,
                "limit": 10,
                "offset": 0,
                "year_offset": 0,
            }
        }
    }

    @field_validator("limit")
    def validate_limit(value):
        if value > config.search_limit_per_query:
            raise ValueError(
                "Search limit value exceeds total possible limit set"
                f" per query {config.search_limit_per_query}"
            )
        return value


class V2SearchResultsItem(BaseModel):
    """Movie search results"""

    id: int = Field(description="Movie identity number")
    title: str = Field(description="Movie title name")
    genres: list[
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
    ] = Field(description="Movie genre names")
    category: t.Literal["Bollywood", "Hollywood"] = Field(
        description="Movie category name as in Bollywood etc"
    )
    year: t.Optional[PositiveInt] = Field(
        None, description="Movie official releas year"
    )
    distribution: t.Literal[
        "BluRay",
        "WEB-DL",
        "HDRip",
        "DVDR",
        "WEBRip",
        "BRRip",
        "DVDRip",
        "CAMRip",
        "HDTV",
        "BDRip",
        "Unknown",
        "DVDRip720p",
        "DVDSCR",
        "PDVDRip",
        "TS",
        "VODRip",
        "R5",
    ] = Field(description="Movie ditribution format name")
    description: t.Optional[str] = Field(None, description="Movie about a.k.a plot")
    url: HttpUrl = Field(description="Link to pointing to the movie page on host")
    cover_photo: HttpUrl = Field(description="Link pointing to movie album photo")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "title": "Aladdin",
                "genres": [
                    "Musical",
                    "Comedy",
                    "Fantasy",
                    "Adventure",
                    "Romance",
                    "Music",
                    "Family",
                ],
                "category": "Hollywood",
                "year": 2019,
                "distribution": "BluRay",
                "description": (
                    "A kindhearted street urchin and a power-hungry Grand Vizier"
                    "model_config vie for a magic lamp that has the power to make their deepest wishes come true."
                ),
                "url": "https://fzmovies.net/movie-Aladdin--hmp4.htm",
                "cover_photo": "https://fzmovies.net/imdb_images/Aladdin.2019.jpg",
            }
        }
    }


class V2SearchResults(BaseModel):
    """List of movies found"""

    query: str = Field(description="Search query")
    movies: list[V2SearchResultsItem] = Field(description="List of movies matched")

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "Love",
                "movies": [
                    {
                        "id": 467,
                        "title": "To Rome with Love",
                        "genres": ["Comedy", "Romance"],
                        "category": "Hollywood",
                        "year": 2012,
                        "distribution": "BluRay",
                        "description": "Set in the romantic city of Rome. The intertwining stories of a worker who wakes up to find himself a celebrity, an architect who takes a trip back to the street he lived on as a student, a young couple on their honeymoon, and a frustrated opera director who has a talent for discovering talented singers. ...<more>",
                        "url": "https://fzmovies.net/movie-To%20Rome%20with%20Love--hmp4.htm",
                        "cover_photo": "https://fzmovies.net/imdb_images/To%20Rome%20with%20Love.jpg",
                    },
                    {
                        "id": 1970,
                        "title": "Dorfman in Love",
                        "genres": ["Drama", "Comedy", "Romance"],
                        "category": "Hollywood",
                        "year": 2012,
                        "distribution": "BluRay",
                        "description": "Unknowingly trapped in her role as caretaker of her unappreciative family, a young single woman desperately needs to get her own life. When she volunteers to cat sit at her unrequited love's downtown L.A. loft, her world, as she knows it, changes forever. ...<more>",
                        "url": "https://fzmovies.net/movie-Dorfman%20in%20Love%20--hmp4.htm",
                        "cover_photo": "https://fzmovies.net/imdb_images/Dorfman.in.Love.2011.jpg",
                    },
                ],
            }
        }
    }
