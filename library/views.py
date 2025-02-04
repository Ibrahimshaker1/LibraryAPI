import time
from fuzzywuzzy import fuzz
from django.contrib.auth import authenticate
from datetime import datetime
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import BookSerializer, AuthorSerializer, RegisterSerializer
from . import models
# const
def change_title(book: models.Books, new_title: str):
    book.title = new_title
def change_rate(book: models.Books, new_rate: int):
    book.rate = int(new_rate)
def change_lag(book: models.Books, new_lag: str):
    book.lag = new_lag
def change_pages(book: models.Books, new_pages: int):
    book.pages = int(new_pages)
def change_publication_date(book: models.Books, new_publication_date):
    new_publication_date = datetime.strptime(new_publication_date, "%Y-%m-%d").date()
    if new_publication_date > datetime.now().date():
        raise("Date Error")
    else:
        book.publication_date = new_publication_date
def change_publisher(book: models.Books, new_publisher: str):
    book.publisher = new_publisher
def change_author(book: models.Books, new_author: str):
    books_authors = book.author.all()
    for book_author in books_authors:
        book_author.delete()
    new_author = new_author.replace(" ", "").split("/")
    for author in new_author:
        author_list = models.Authors.objects.filter(name=author.lower())
        if len(author_list) > 0:
            new_book_author = models.BooksAuthors(
                book=book,
                author=author_list[0]
            )
            new_book_author.save()
        else:
            my_new_author = models.Authors(
                name = author.lower()
            )
            new_book_author = models.BooksAuthors(
                book=book,
                author=my_new_author
            )
            my_new_author.save()
            new_book_author.save()


update_book_func = {
    "title": change_title,
    "rate": change_rate,
    "lag": change_lag,
    "pages": change_pages,
    "publication_date": change_publication_date,
    "publisher": change_publisher,
    "author": change_author
}

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class Books(APIView):
    def get_permissions(self):
        if self.request and self.request.method == "GET":
            return [AllowAny()]
        return [AllowAny()]


    def get(self, request, format=None):
        books = models.Books.objects.all()
        books_list = []
        author = []
        if len(books) > 0:
            for book in books:
                if len(book.author.filter(book=book)) > 1:
                    for book_author in book.author.filter(book=book):
                        author.append(book_author.author.name)
                else:
                    author.append(book.author.get(book=book).author.name)
                book_data = {
                    "id": book.id,
                    "title": book.title,
                    "authors": author,
                    "rate": book.rate,
                    "lang": book.lag,
                    "pages": book.pages,
                    "publication_date": book.publication_date,
                    "publisher": book.publisher
                }
                books_list.append(book_data)
                author = []
            return Response({
                "data": books_list,
                "books_number": len(books_list)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "no books"
            }, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        request_data = BookSerializer(data=request.data)
        if request_data.is_valid():
            try:
                book_input_data = request_data.data
                book = models.Books(
                    title=book_input_data['title'],
                    rate=book_input_data['rate'],
                    lag=book_input_data['lag'],
                    pages=book_input_data['pages'],
                    publication_date=book_input_data['publication_date'],
                    publisher=book_input_data['publisher']
                )
                book.save()
                author_list = book_input_data['author'].replace(" ", "").split("/")
                for my_author in author_list:
                    author = models.Authors.objects.filter(name=my_author.lower())
                    if len(author) > 0:
                        book_author = models.BooksAuthors(
                            book=book,
                            author=author[0]
                        )
                        book_author.save()
                    else:
                        author = models.Authors(
                            name=my_author.lower()
                        )
                        if author:
                            book_author = models.BooksAuthors(
                                book=book,
                                author=author
                            )
                            author.save()
                            book_author.save()
                return Response(
                    {
                        "message": "Book is Created",
                        "data": model_to_dict(book)
                    }, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response(
                    {
                        "message": "Create Book Error"
                    }, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            return Response({
                 "message": "data is not valid"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)


class BookUpdateDelete(APIView):
    permission_classes = [AllowAny]

    def put(self, request, book_id, format=None):
        book_id = book_id
        book = models.Books.objects.filter(id=book_id)
        if len(book) > 0:
            print(request.data)
            for my_key in request.data.keys():
                update_book_func[my_key](book[0], request.data[my_key])
            book[0].save()
            return Response({
                "massage": "book is here",
                "data": model_to_dict(book[0])
            })
        else:
            return Response({
                "message": "Book Not Here",
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id, format=None):
        book = models.Books.objects.filter(id=book_id)
        if len(book) > 0:
            book[0].delete()
            return Response({
                "message": f"Book with ID: {book_id} Deleted"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Book is not found"
            }, status=status.HTTP_400_BAD_REQUEST)

## Author APIs


class Authors(APIView):
    def get_permissions(self):
        if self.request and self.request.method == "GET":
            return [AllowAny()]
        else:
            return[AllowAny()]

    def get(self, request, format=None):
        authors_list = []
        authors = models.Authors.objects.all()
        for author in authors:
            book_list = []
            author_books = author.book.all()
            for book_author in author_books:
                book_list.append(book_author.book.title)
            author_dict = {
                "id": author.id,
                "name": author.name,
                "books": book_list
            }
            authors_list.append(author_dict)
        return Response({
            "data": authors_list
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        author = AuthorSerializer(data=request.data)
        if author.is_valid():
            author.save()
            return Response({
                "message": "author created!",
                "data": author.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message":  "invalid data"
            }, status=status.HTTP_400_BAD_REQUEST)


class AuthorUpdateDelete(APIView):
    permission_classes = [AllowAny]
    def put(self, request, author_id, format=None):
        new_name = request.data['name'].lower()
        if new_name:
            author = models.Authors.objects.filter(id=author_id)
            other_author = models.Authors.objects.filter(name=new_name)
            if len(author) > 0 and len(other_author) == 0:
                author[0].name = new_name
                author[0].save()
                return Response({
                    "message": "author updated",
                    "data": model_to_dict(author[0])
                }, status=status.HTTP_200_OK)
            elif len(other_author) > 0:
                return Response({
                    "message": "author name is used"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "message": "author not found"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "message": "parame name is 'name'"
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, author_id, format=None):
        author = models.Authors.objects.filter(id=author_id)
        books_authors = author[0].book.all()
        can_delete = False
        if len(books_authors) > 0:
            for book_author in books_authors:
                book = book_author.book
                book_authos_book = book.author.all()
                if len(book_authos_book) > 1:
                    can_delete = True
        else:
            can_delete = True

        if len(author) > 0 and can_delete:
            author.delete()
            return Response({
                "message": "author deleted"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "author not found or author cant de deleted"
            }, status=status.HTTP_400_BAD_REQUEST)


# return one object


class Book(APIView):
    permission_classes = [AllowAny]

    def get(self, request, book_id, format=None):
        book = models.Books.objects.filter(id=book_id)
        if len(book) > 0:
            author_list = []
            authors = book[0].author.all()
            for book_author in authors:
                author_list.append(book_author.author.name)
            return Response({
                "data": model_to_dict(book[0]),
                "authors": author_list
            })
        else:
            return Response({
                "message": "Book no found"
            })


class Author(APIView):
    permission_classes = [AllowAny]

    def get(self, request, author_id, format=None):
        author = models.Authors.objects.filter(id=author_id)
        if len(author) > 0:
            return Response({
                "data": model_to_dict(author[0])
            })
        else:
            return Response({
                "message": "author no found"
            })

## Search API


class SearchAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        title = request.GET.get("title", "none")
        author = request.GET.get("author", "none")
        book_list = []
        if title != "none":
            title = title.title()
            books = models.Books.objects.filter(title=title)
            if len(books) > 0:
                for book in books:
                    book_list.append(model_to_dict(book))
                return Response({
                    "message": "search by title",
                    "data": book_list
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "book not found"
                }, status=status.HTTP_400_BAD_REQUEST)
        elif author != "none":
            author = author.lower()
            author = models.Authors.objects.filter(name=author)
            if len(author) > 0:
                books_authors = author[0].book.all()
                if len(books_authors) > 0:
                    for book_author in books_authors:
                        book = book_author.book
                        book_list.append(model_to_dict(book))
                    return Response({
                        "message": "Search by author",
                        "data": book_list
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "author have no books",
                        "data": book_list
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "author do not found",
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "wrong query name you can search be 'title' ro 'author'",
            }, status=status.HTTP_400_BAD_REQUEST)

# add Favorites Book
class GetFavoriteList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        book_list = []
        favorite_books = user.favorite_books.all()
        if len(favorite_books) > 0:
            for favorite_book in favorite_books:
                book = favorite_book.book
                book_list.append(model_to_dict(book))
            return Response({
                "message": "user favorite list",
                "data": book_list
            })
        else:
            return Response({
                "message": "user do not have favorite book"
            }, status=status.HTTP_404_NOT_FOUND)


class FavoriteBook(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id,format=None):
        user = request.user
        user_favorite_books = user.favorite_books.all()
        if len(user_favorite_books) < 20:
            book_list = models.Books.objects.filter(id=book_id)
            if len(book_list) > 0:
                book = book_list[0]
                book_users = book.favorite_users.all()
                for user_f_book in user_favorite_books:
                    if user_f_book in book_users:
                        return Response({
                            "message": "book already in favorites"
                        }, status=status.HTTP_406_NOT_ACCEPTABLE)
                favorite = models.Favorites(
                    user=user,
                    book=book
                )
                favorite.save()
                time_one = time.perf_counter()
                sg_book_list = []
                books = models.Books.objects.exclude(id=book.id)
                for a_book in books:
                    if a_book.lag == book.lag:
                        if a_book.author == book.author:
                            sg_book_list.append(model_to_dict(a_book))
                            if len(sg_book_list) == 5:
                                break
                        else:
                            title_score = fuzz.partial_ratio(book.title.lower(), a_book.title.lower())
                            if title_score > 65:
                                sg_book_list.append(model_to_dict(a_book))
                                if len(sg_book_list) == 5:
                                    break
                time_two = time.perf_counter()
                result = time_two - time_one
                print(f"Time in Second: {result:.6f}")
                return Response({
                    "message": "added to favorite book list",
                    "data": model_to_dict(book),
                    "suggested_books": sg_book_list
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "Book Not Found"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "message": "you already have 20 favorite book",
            }, status=status.HTTP_406_NOT_ACCEPTABLE
            )



