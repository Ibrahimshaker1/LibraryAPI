from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Authors(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Books(models.Model):
    title = models.TextField()
    rate = models.IntegerField()
    lag = models.CharField(max_length=255)
    pages = models.IntegerField()
    publication_date = models.DateField()
    publisher = models.TextField()

    def __str__(self):
        return self.title


class BooksAuthors(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="author")
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, related_name="book")


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_books")
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name="favorite_users")
