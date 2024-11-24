from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from backend.config import config
from backend.utils import utcnow

engine = create_engine(config.database_engine)
"""Initialized db engine"""

Base = declarative_base()

Session = sessionmaker(bind=engine)
"""Un-initialized db session"""

session = Session()
"""Initialized db session"""


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)
    movies = relationship(
        "Movie",
        uselist=True,
        passive_deletes=True,
        backref="category",
    )

    def __str__(self):
        return self.name


class MovieGenre(Base):
    __tablename__ = "movie_genre"
    id = Column(Integer, primary_key=True)
    movie_id = Column(
        Integer,
        ForeignKey("movie.id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    genre_id = Column(
        Integer,
        ForeignKey("genre.id", onupdate="CASCADE", ondelete="CASCADE"),
    )


class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True, nullable=False)
    movies = relationship("Movie", secondary="movie_genre", back_populates="genres")

    def __str__(self):
        return self.name


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    title = Column(String(30), unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    distribution = Column(String(15), nullable=True)
    description = Column(Text, nullable=True)
    url = Column(String(50), nullable=False)
    cover_photo = Column(String(70), nullable=False)
    genres = relationship("Genre", secondary="movie_genre", back_populates="movies")
    category_id = Column(
        Integer,
        ForeignKey(
            "category.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )

    def model_dump(self) -> dict[str, int | str]:
        return dict(
            id=self.id,
            title=self.title,
            year=self.year,
            distribution=self.distribution,
            description=self.description,
            url=self.url,
            cover_photo=self.cover_photo,
            category=self.category.name,
            genres=[genre.name for genre in self.genres],
        )

    def __str__(self):
        return f"{self.title} ({self.year})"


class NormalDownloadLink(Base):
    __tablename__ = "normal_download_link"
    id = Column(Integer, primary_key=True)
    filename = Column(String(60), nullable=False)
    url = Column(Text, nullable=False)
    updated_on = Column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
    )

    def model_dump(self) -> dict[str, str]:
        return dict(filename=self.filename, url=self.url)


class BestDownloadLink(Base):
    __tablename__ = "best_download_link"
    id = Column(Integer, primary_key=True)
    filename = Column(String(60), nullable=False)
    url = Column(Text, nullable=False)
    updated_on = Column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
    )

    def model_dump(self) -> dict[str, str]:
        return dict(filename=self.filename, url=self.url)


def create_tables(drop_all: bool = False):
    if drop_all:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
