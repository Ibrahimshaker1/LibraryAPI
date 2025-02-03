from django.urls import path
from .views import Books, RegisterView, LoginView, BookUpdateDelete, Authors, Book, Author, AuthorUpdateDelete

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("Books/", Books.as_view(), name="books"),
    path("Book/<int:book_id>", Book.as_view(), name="book"),
    path("BookEdite/<int:book_id>", BookUpdateDelete.as_view(), name="book_edite"),
    path("Authors/", Authors.as_view(), name="authors"),
    path("Author/<int:author_id>", Author.as_view(), name="author"),
    path("AuthorEdite/<int:author_id>", AuthorUpdateDelete.as_view(), name="auhtor_edite")
]
