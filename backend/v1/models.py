"""Pydantic Models"""

from pydantic import BaseModel, PositiveInt, field_validator, HttpUrl
import typing as t
from backend.config import config
import re
from fzmovies_api.models import MovieFiles as FzMovieFiles
from fzmovies_api.models import SearchResults as FzSearchResults
from fzmovies_api.models import MovieInSearch as FzMovieInSearch


class Search(BaseModel):
    """Search movies by Name|Director|Startcast
    - `q` : Search query
    - `searchby` : Search filter
    - `category` : Search category
    - `limit` : Search results limit. Multiple of 20.
    - `offset` : Value to truncate search results from.
    """

    q: str
    searchby: t.Optional[t.Literal["Name", "Director", "Starcast"]] = "Name"
    category: t.Optional[t.Literal["All", "Bollywood", "Hollywood", "DHollywood"]] = (
        "All"
    )
    limit: t.Optional[PositiveInt] = 20
    offset: t.Optional[int] = 0

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "q": "Fast and Furious",
                    "searchby": "Name",
                    "category": "Hollywood",
                    "limit": 10,
                    "offset": 0,
                },
                {
                    "q": "Jason Statham",
                    "searchby": "Starcast",
                    "category": "Hollywood",
                    "limit": 30,
                    "offset": 5,
                },
                {
                    "q": "James Cameron",
                    "searchby": "Director",
                    "category": "All",
                    "limit": 50,
                    "offset": 0,
                },
            ],
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

    @field_validator("offset")
    def validate_offset(value):
        if value < 0:
            raise ValueError("Input should be greater than 0")
        return value


class SearchStream(BaseModel):
    """Search movies by Name|Director|Startcast and stream results
    - `q` : Search query
    - `searchby` : Search filter
    - `category` : Search category
    - `limit` : Search results limit. Multiple of 20.
    - `offset` : Value to truncate search results from.
    """

    q: str
    searchby: t.Optional[t.Literal["Name", "Director", "Starcast"]] = "Name"
    category: t.Optional[t.Literal["All", "Bollywood", "Hollywood", "DHollywood"]] = (
        "All"
    )
    limit: t.Optional[PositiveInt] = 20

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "q": "Wrong Turn",
                    "searchby": "Name",
                    "category": "Hollywood",
                    "limit": 9,
                    "offset": 0,
                },
                {
                    "q": "Dwayne Johnson",
                    "searchby": "Starcast",
                    "category": "Hollywood",
                    "limit": 20,
                    "offset": 0,
                },
                {
                    "q": "James Cameron",
                    "searchby": "Director",
                    "category": "Hollywood",
                    "limit": 20,
                    "offset": 0,
                },
            ],
        }
    }

    @field_validator("limit")
    def validate_limit(value):
        if value > config.search_stream_limit_per_query:
            raise ValueError(
                "Search limit value exceeds total possible limit set"
                f" per query {config.search_limit_per_query} - {value}"
            )
        return value


class TargetMovie(BaseModel):
    """Get metadata for a particular movie
    - `movie_page_url`: Link to the page containing info about the targeted movie.
    """

    movie_page_url: HttpUrl

    model_config = {
        "json_schema_extra": {
            "example": {
                "movie_page_url": "https://fzmovies.net/movie-Fast%20and%20Furious%207--hmp4.htm"
            }
        }
    }

    @field_validator("movie_page_url")
    def validate_url(value):
        if re.match(
            r"https://(tvseries.in|mobiletvshows.site|fztvseries.live)/movie-.+\.htm$",
            str(value),
        ):
            raise ValueError(f"Invalid url passed.")
        return value


class TargetFilename(BaseModel):
    """Get download link for a particular filename
    - `filename_url`: Link to the targeted movie file.
    """

    filename_url: HttpUrl

    model_config = {
        "json_schema_extra": {
            "example": {
                "filename_url": "https://fzmovies.net/download1.php?downloadoptionskey=5-26561-0b2a165834258d475c6ce9b3c1608bdf"
            }
        }
    }

    @field_validator("filename_url")
    def validate_url(value):
        if re.match(
            r"https://(tvseries.in|mobiletvshows.site|fztvseries.live)/download1\.php\?downloadoptionskey=[\w_-]+$",
            str(value),
        ):
            raise ValueError(f"Invalid url passed.")
        return value


class DownloadLink(BaseModel):
    """Get link pointing to downloadable file
    - `filename`: Movie filename
    -  `url`: Link to downlodable movie file.
    """

    filename: str
    url: HttpUrl

    model_config = {
        "json_schema_extra": {
            "example": {
                "filename": "Fast_and_Furious_7_BluRay_high.mp4",
                "url": "https://ik2mqisu1w.b34zobxzxs73nkfxike1.cfd/res/614774a84bca32182e1b81d831542d9a/e5f8078be8df179e5497e448dc163aaf/Fast_and_Furious_7_(2015)_BluRay_high_(fzmovies.net)_f54b7581dcde1c46de8365af485a3836.mp4?fromwebsite",
            }
        }
    }


class SearchResults(FzSearchResults):

    model_config = {
        "json_schema_extra": {
            "example": {
                "movies": [
                    {
                        "url": "https://fzmovies.net/movie-Fast%20and%20Furious%20Presents%20-%20Hobbs%20and%20Shaw--hmp4.htm",
                        "title": "Fast and Furious Presents - Hobbs and Shaw",
                        "year": 2019,
                        "distribution": "BluRay",
                        "about": "Lawman Luke Hobbs and outcast Deckard Shaw form an unlikely alliance when a cyber-genetically enhanced villain threatens the future of humanity.",
                        "cover_photo": "https://fzmovies.net/imdb_images/Hobbs.and.Shaw.2019.jpg",
                    },
                    {
                        "url": "https://fzmovies.net/movie-Fast%20and%20Furious%209--hmp4.htm",
                        "title": "Fast and Furious 9",
                        "year": 2021,
                        "distribution": "BluRay",
                        "about": "Cypher enlists the help of Jakob, Dom's younger brother to take revenge on Dom and his team.",
                        "cover_photo": "https://fzmovies.net/imdb_images/Fast.And.Furious.9.2021.jpg",
                    },
                ],
                "first_page": None,
                "previous_page": None,
                "next_page": None,
                "last_page": None,
            }
        }
    }


class MovieFiles(FzMovieFiles):

    model_config = {
        "json_schema_extra": {
            "example": {
                "files": [
                    {
                        "title": "The Manson Family BluRay 480p.mp4",
                        "url": "https://fzmovies.net/download1.php?downloadoptionskey=3-41760-750fa9a3ff2cefd8f133cb6e42ba679e",
                        "size": "253 MB",
                        "hits": 2160,
                        "mediainfo": "https://fzmovies.net/mediainfo.php?downloadoptionskey=3-41760-750fa9a3ff2cefd8f133cb6e42ba679e",
                        "ss": "https://fzmovies.net/ss.php?downloadoptionskey=3-41760-750fa9a3ff2cefd8f133cb6e42ba679e",
                    },
                    {
                        "title": "The Manson Family BluRay 720p.mkv",
                        "url": "https://fzmovies.net/download1.php?downloadoptionskey=5-39728-84d89bd8c2c6a1476ce244293acc623a",
                        "size": "678 MB",
                        "hits": 111,
                        "mediainfo": "https://fzmovies.net/mediainfo.php?downloadoptionskey=5-39728-84d89bd8c2c6a1476ce244293acc623a",
                        "ss": "https://fzmovies.net/ss.php?downloadoptionskey=5-39728-84d89bd8c2c6a1476ce244293acc623a",
                    },
                ],
                "trailer": None,
                "recommended": [
                    {
                        "title": "Assassins Run",
                        "url": "https://fzmovies.net/movie-Assassins%20Run--hmp4.htm",
                        "cover_photo": "https://fzmovies.net/imdb_images/Assassins%20Run.jpg",
                    },
                    {
                        "title": "The Shawshank Redemption",
                        "url": "https://fzmovies.net/movie-The%20Shawshank%20Redemption--hmp4.htm",
                        "cover_photo": "https://fzmovies.net/imdb_images/The%20Shawshank%20Redemption.jpg",
                    },
                    {
                        "title": "The Lost Legion",
                        "url": "https://fzmovies.net/movie-The%20Lost%20Legion--hmp4.htm",
                        "cover_photo": "https://fzmovies.net/imdb_images/The.Lost.Legion.2014.jpg",
                    },
                ],
            }
        }
    }
