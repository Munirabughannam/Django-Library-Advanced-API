from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.InventoryView.as_view()),
    path('cart/', views.UserCartView.as_view()),
    path('reserve/', views.ReservingBooksView.as_view()),
    path('reservations/', views.CheckedOutBooksView.as_view()),
    path('reservations/<int:pk>', views.CheckedOutBooksSingleView.as_view()),
    path('admin/reservations', views.LibrarianView.as_view()),
    path('admin/reservations/<int:pk>', views.LibrarianSingleView.as_view()),

]