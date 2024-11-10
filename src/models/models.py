import uuid

from sqlalchemy import UUID, String, Integer, ForeignKey, Column, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    def as_dict(self):
        return {c.full_name: getattr(self, c.full_name) for c in self.__table__.columns}


author_tag_association = Table(
    "author_tag",
    Base.metadata,
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)

book_tag_association = Table(
    "book_tag",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class AuthorModel(Base):
    __tablename__ = "authors"

    full_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    country: Mapped[str] = mapped_column(String, index=True, nullable=False)

    books: Mapped[list["BookModel"]] = relationship(
        "BookModel", back_populates="author"
    )

    tags: Mapped[list["TagModel"]] = relationship(
        "TagModel", secondary="author_tag", back_populates="authors"
    )

    def __repr__(self):
        return f"<AuthorModel(full_name={self.full_name}, country={self.country})>"


class BookModel(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=True)

    author_id: Mapped[UUID] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[AuthorModel] = relationship("AuthorModel", back_populates="books")

    tags: Mapped[list["TagModel"]] = relationship(
        "TagModel", secondary="book_tag", back_populates="books"
    )

    def __repr__(self):
        return f"<Book(title={self.title}, genre={self.genre}, created_at={self.created_at})>"


class TagModel(Base):
    __tablename__ = "tags"

    tag_title: Mapped[str] = mapped_column(String, nullable=False)

    authors: Mapped[list[AuthorModel]] = relationship(
        "AuthorModel", secondary="author_tag", back_populates="tags"
    )

    books: Mapped[list[BookModel]] = relationship(
        "BookModel", secondary="book_tag", back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag(tag_title={self.tag_title})>"
