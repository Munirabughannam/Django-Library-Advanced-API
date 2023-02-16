# imported necessary modules
from django.db import models
from django.contrib.auth.models import User


# Create a model for the library inventory
class LibraryInventory(models.Model):
    # Defining model fields
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)

    # return the title of the book as the string representation
    def __str__(self):
        return self.title

# Create a model for a user's cart
class UserCart(models.Model):
    # Defining model fields
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Define a foreign key relationship to the User model
    books = models.ForeignKey(LibraryInventory, on_delete=models.CASCADE) # Define a foreign key relationship to the LibraryInventory model
    quantity = models.SmallIntegerField(default=1)


# Create a model for reserving books
class ReservingBooks(models.Model):
    # Defining model fields
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Define a foreign key relationship to the User model


# Create a model for checked-out books
class CheckedOutBooks(models.Model):
    # Defining model fields
    order = models.ForeignKey(ReservingBooks, on_delete=models.CASCADE) # Define a foreign key relationship to the ReservingBooks model
    reserved_books = models.ForeignKey(LibraryInventory, on_delete=models.CASCADE) # Define a foreign key relationship to the LibraryInventory model
    quantity = models.SmallIntegerField(default=0)
