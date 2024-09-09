from rest_framework import serializers
from .models import Author, Book

# BookSerializers
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validaton that ensure the publication year is not in the future
    def publication_year_IsValid(self, value):
        from datetime import datetime
        current_yr = datetime.date.today().year
        if value > current_yr:
            raise serializers.ValidationError("The publication is in the Future which is INVALID!")
        return value
    

# AUthorSerializer and nested book
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)   #Nested serializer to include books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

        