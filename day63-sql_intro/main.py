# PART 1
# import sqlite3

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

# PART 2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new_books_collection.db"
db.init_app(app)


class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


# with app.app_context():
#     db.create_all()

# with app.app_context():
#     book = Books(
#         title="Harry Potter",
#         author="J. K. Rowling",
#         rating=9.3
#     )
#     db.session.add(book)
#     db.session.commit()


# with app.app_context():
#     result = db.session.execute(db.select(Books).order_by(Books.title))
#     all_books = result.scalars()
#     print(all_books.first())
#
#
# with app.app_context():
#     book = db.session.execute(db.select(Books).where(Books.title == "Harry Potter")).scalar()
#
#     book_to_update = book
#     book_to_update.title = "Harry Potter and the Chamber of Secrets"
#     db.session.commit()


book_id = 1
with app.app_context():
    book_to_update = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
    book_to_update.title = "Harry Potter and the Goblet of Fire"
    db.session.commit()

# with app.app_context():
#     book_to_delete = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
#     # or book_to_delete = db.get_or_404(Book, book_id)
#     db.session.delete(book_to_delete)
#     db.session.commit()
