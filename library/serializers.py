from rest_framework import serializers
from .models import Authors, User
from datetime import datetime

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = '__all__'

    def create(self, validate_data):
        author = Authors.objects.create(**validate_data)
        return author


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=65535)
    rate = serializers.IntegerField()
    lag = serializers.CharField(max_length=255)
    pages = serializers.IntegerField()
    publication_date = serializers.DateField()
    publisher = serializers.CharField(max_length=255)
    author = serializers.CharField(max_length=255)

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title Can not by empty")
        return value.title()

    def validate_publication_date(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("Date Error")
        return value







