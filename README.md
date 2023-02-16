# Django-Library-Advanced-API

This project is a library management system that allows users to check-out and reserve books. The project uses the Django web framework and Djoser, a module for implementing token-based authentication. Users can register and request authentication tokens to use the API's provided. The API supports various features like pagination, filtering and search. The response is returned in JSON format.

The project includes four models: LibraryInventory, UserCart, CheckedOutBooks, and ReservingBooks. The LibraryInventory model contains the title, author, and quantity of the books in the library. Users can add books to their UserCart model and specify the quantity they want to borrow. The CheckedOutBooks model represents the checked-out items with information about the order, reserved book, and quantity. The ReservingBooks model stores information about the user who has reserved the book and the date of the reservation.

The project includes several RESTful APIs to support the functionality of the library management system. Users can check-out, reserve books, and get information about the books in the library such as quantity avaialble. The API also supports pagination, filtering, and searching for books. The API uses token-based authentication to ensure that only authorized users can access the API's.

Overall, the project provides a comprehensive way for managing a library system with various features such as user registration, book checkout, reservation, admin management of orders and admin management of inventory.
