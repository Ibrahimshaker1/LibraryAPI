from django.urls import path
from .views import Books, RegisterView, LoginView, BookUpdateDelete, Authors, Book, Author, AuthorUpdateDelete, SearchAPI,  FavoriteBook, GetFavoriteList

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("Books/", Books.as_view(), name="books"),
    path("Book/<int:book_id>", Book.as_view(), name="book"),
    path("BookEdite/<int:book_id>", BookUpdateDelete.as_view(), name="book_edite"),
    path("Authors/", Authors.as_view(), name="authors"),
    path("Author/<int:author_id>", Author.as_view(), name="author"),
    path("AuthorEdite/<int:author_id>", AuthorUpdateDelete.as_view(), name="author_edite"),
    path("Search/", SearchAPI.as_view(), name="search"),
    path("FavoriteBook/<int:book_id>", FavoriteBook.as_view(), name="favorite_book"),
    path("GetFavorite/", GetFavoriteList.as_view(), name="favorite_list")
]
