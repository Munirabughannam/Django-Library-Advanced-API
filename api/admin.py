# imported necessary modules
from django.contrib import admin
from .models import *

# Registered the four models in models.py.
admin.site.register(LibraryInventory)
admin.site.register(UserCart)
admin.site.register(CheckedOutBooks)
admin.site.register(ReservingBooks)
