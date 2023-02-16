# imported necessary modules
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


# view for listing and creating inventory items
class InventoryView(generics.ListCreateAPIView):
    # set queryset, serializer, ordering and search fields
    queryset = LibraryInventory.objects.all()
    serializer_class = InventorySerializer
    ordering_fields = ['title']
    search_fields = ['title', 'author']

    # get permissions based on request method
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


# view for listing and creating items in the user's cart
class UserCartView(generics.ListCreateAPIView):
    # set permission class and serializer
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    # get items in the cart for the current user
    def get_queryset(self):
        user = self.request.user
        return UserCart.objects.filter(user=user)

    # create an item in the user's cart
    def perform_create(self, serializer):
        if serializer.is_valid():
            book = serializer.validated_data['books']
            library_inventory = book
            # checking if the quantity of item in library inventory
            if library_inventory.quantity > 0:
                if library_inventory.quantity >= serializer.validated_data['quantity']:
                    # update the library inventory and add the item to the user's cart
                    library_inventory.quantity -= serializer.validated_data['quantity']
                    library_inventory.save()
                    user = self.request.user
                    serializer.save(user=user)
                else:
                    # raise an error if there are not enough items in the library inventory
                    raise serializers.ValidationError('The quantity of this item in the library is not enough')
            else:
                # raise an error if the quantity in the library inventory is 0
                raise serializers.ValidationError('The quantity of this item in the library is 0')

    # delete all items in the user's cart and updates the library inventory
    def delete(self, request):
        user = self.request.user
        cart = UserCart.objects.filter(user=user)
        for item in cart:
            book = item.books
            library_inventory = book
            library_inventory.quantity += item.quantity
            library_inventory.save()
        cart.delete()
        return Response(status=204)


# view for listing and creating items that the user has reserved
class ReservingBooksView(generics.ListCreateAPIView):
    # set permission class and serializer
    serializer_class = ReservingSerializer
    permission_classes = [IsAuthenticated]

    # get items that the user has reserved
    def get_queryset(self):
        user = self.request.user
        return ReservingBooks.objects.filter(user=user)

    # create an order for reserved items and update the checked out items
    def perform_create(self, serializer):
        cart_items = UserCart.objects.filter(user=self.request.user)
        order = serializer.save(user=self.request.user)
        for cart_item in cart_items:
            CheckedOutBooks.objects.create(reserved_books=cart_item.books, quantity=cart_item.quantity, order=order)
            cart_item.delete()


# view for listing checked out items for the current user
class CheckedOutBooksView(generics.ListAPIView):
    # set permission class and serializer
    serializer_class = CheckedOutBooksSerializer
    permission_classes = [IsAuthenticated]

    # get checked out items for the current user
    def get_queryset(self):
        user = self.request.user
        return ReservingBooks.objects.filter(user=user)


# Single item view for checked out items
class CheckedOutBooksSingleView(generics.RetrieveAPIView):
    # set permission class and serializer
    serializer_class = CheckedOutBooksSerializer
    permission_classes = [IsAuthenticated]

    # get checked out items for the current user
    def get_queryset(self):
        user = self.request.user
        return ReservingBooks.objects.filter(user=user)

    # delete all items in the user's checked out books and updates the library inventory
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        reservation = ReservingBooks.objects.get(pk=pk)
        items = CheckedOutBooks.objects.filter(order=reservation)
        for item in items:
            Library_Book = item.reserved_books
            quantity = item.quantity
            Library_Book.quantity += quantity
            Library_Book.save()
            item.delete()
        reservation.delete()
        return Response(status=204)


# Admin view for listing checked out items for all users
class LibrarianView(generics.ListAPIView):
    # set permission class, serializer and search fields
    serializer_class = CheckedOutBooksSerializer
    queryset = ReservingBooks.objects.all()
    search_fields = ['user__id', 'user__username']


# Admin view for retrieving single reservations
class LibrarianSingleView(generics.RetrieveAPIView):
    # set permission class and serializer
    serializer_class = CheckedOutBooksSerializer
    queryset = ReservingBooks.objects.all()
