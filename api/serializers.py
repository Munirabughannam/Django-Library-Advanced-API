# imported necessary modules
from rest_framework import serializers
from .models import *


# Serializer for the LibraryInventory model
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryInventory
        # Serialize the following fields
        fields = ['id', 'title', 'author', 'quantity']


# Serializer for the UserCart model
class CartSerializer(serializers.ModelSerializer):
    Book = serializers.CharField(source='books.title', read_only=True)
    Username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserCart
        # Serialize the following fields
        fields = ['Username', 'books', 'Book', 'quantity']

        # Ensure the books field is write-only
        extra_kwargs = {
            'books': {'write_only': True},
        }


# Serializer for the ReservingBooks model
class ReservingSerializer(serializers.ModelSerializer):
    Books = serializers.SerializerMethodField()

    class Meta:
        model = ReservingBooks
        # Serialize the following fields
        fields = ['id', 'date', 'user', 'Books']

        # Ensure the user field is read-only
        extra_kwargs = {
            'user': {'read_only': True},
        }

    # Retrieve the reserved books in this reservation
    def get_Books(self, obj):
        cart = CheckedOutBooks.objects.filter(order=obj)
        serializer = HelperSerializer(cart, many=True, context={'request': self.context['request']})
        return serializer.data


# Helper serializer for the CheckedOutBooks model
class HelperSerializer(serializers.ModelSerializer):
    Book = serializers.CharField(source='reserved_books.title', read_only=True)
    Author = serializers.CharField(source='reserved_books.author', read_only=True)

    class Meta:
        model = CheckedOutBooks
        # Serialize the following fields
        fields = ['Book', 'Author', 'quantity']


# Serializer for the CheckedOutBooks model
class CheckedOutBooksSerializer(serializers.ModelSerializer):
    Books = serializers.SerializerMethodField()
    Username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ReservingBooks
        # Serialize the following fields
        fields = ['id', 'date', 'user', 'Username', 'Books']

    # Retrieve the checked out books in this reservation
    def get_Books(self, obj):
        cart = CheckedOutBooks.objects.filter(order=obj)
        serializer = HelperSerializer(cart, many=True, context={'request': self.context['request']})
        return serializer.data
