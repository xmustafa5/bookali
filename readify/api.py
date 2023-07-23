from ninja import Router
from pydantic import EmailStr
from CAuth.authorization import AuthBearer
from CAuth.schemas import Four0FourOut
from readify.models import Book, Category, Order, Cart, Address
from readify.schemas import BookOut, BooksOut, CategoryBookOut, CartIn, GetCartOut, OrderIn, DeleteCartIn, \
    AddressOut, OrderBookIn
from rest_framework import status
from django.contrib.auth import get_user_model

readify_router = Router(tags=['readify'])

User = get_user_model()


def get_my_address(user, order_book_in):
    try:
        address = Address.objects.get(user=user, id=order_book_in.address.id)
    except Address.DoesNotExist:
        address = Address.objects.create(
            user=user,
            city=order_book_in.address.city,
            town=order_book_in.address.town,
            nearby=order_book_in.address.nearby,
            phone_number=order_book_in.address.phone_number
        )
    return address


@readify_router.get('/get_all', response={
    200: BooksOut
})
def get_all(request):
    books = Book.objects.all()

    return status.HTTP_200_OK, {'books': list(books)}


@readify_router.get('/get_one', response={
    200: BookOut,
    404: Four0FourOut
})
def get_one(request, book_id: int):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'book not found'}

    return status.HTTP_200_OK, book


@readify_router.get('/get_by_category', response={
    200: list[CategoryBookOut],
    404: Four0FourOut
})
def get_by_category(request,):
    category = Category.objects.all()
    book = [
        {
            'category': category[i].name,
            'books': list(Book.objects.filter(category=category[i])),
        }
        for i in range(len(category))
    ]

    return (
        (status.HTTP_200_OK, book)
        if category
        else (status.HTTP_404_NOT_FOUND, {'detail': 'category not found'})
    )


@readify_router.post('/add_to_cart', response={
    200: Four0FourOut
})
def add_to_cart(request, cart_in: CartIn):
    try:
        user = User.objects.get(email=cart_in.email)
        cart = list(Cart.objects.filter(user=user, book=cart_in.book_id))
        cart[0].quantity += cart_in.quantity
        cart[0].save()
    except IndexError:
        user = User.objects.get(email=cart_in.email)
        book = Book.objects.get(id=cart_in.book_id)
        Cart.objects.create(
            user=user,
            book=book,
            quantity=cart_in.quantity
        )

    return status.HTTP_200_OK, {'detail': 'book added to cart'}


@readify_router.get('/get_cart', response={
    200: GetCartOut
})
def get_cart(request, email: EmailStr):
    user = User.objects.get(email=email)
    cart = Cart.objects.filter(user=user)

    book = [cart_book.book for cart_book in cart]
    total_purchases = sum(
        cart[i].quantity * cart[i].book.price for i in range(len(cart))
    )
    return status.HTTP_200_OK, {'book': book, 'total_price': total_purchases}


@readify_router.get('/get_address', response={
    200: AddressOut
})
def get_address(request, email: EmailStr):
    user = User.objects.get(email=email)
    address = list(Address.objects.filter(user=user))

    return status.HTTP_200_OK, {'address': address}


@readify_router.post('/order', response={
    404: Four0FourOut,
    200: Four0FourOut
})
def order(request, order_in: OrderIn):
    user = User.objects.get(email=order_in.email)
    cart = Cart.objects.filter(user=user)
    if not cart:
        return status.HTTP_404_NOT_FOUND, {'detail': 'cart is empty'}
    books = [cart_book.book for cart_book in cart]

    address = get_my_address(user, order_in)

    orders = Order.objects.create(
        user=user,
        address=address,
    )
    for book in books:
        orders.book.add(book)
    cart.delete()

    return status.HTTP_200_OK, {'detail': 'order created'}


@readify_router.post('/order_book', response={
    200: Four0FourOut,
    404: Four0FourOut
})
def order_book(request, order_book_in: OrderBookIn):
    user = User.objects.get(email=order_book_in.email)

    try:
        book = Book.objects.get(id=order_book_in.book_id)
    except Book.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, {'detail': 'book not found'}

    address = get_my_address(user, order_book_in)

    orders = Order.objects.create(
        user=user,
        address=address,
    )
    orders.book.add(book)

    return status.HTTP_200_OK, {'detail': 'order created'}


@readify_router.delete('/delete_from_cart', response={
    200: Four0FourOut,
    404: Four0FourOut
})
def delete_from_cart(request, delete_cart_in: DeleteCartIn):
    user = User.objects.get(email=delete_cart_in.email)
    books = list(Cart.objects.filter(user=user, book=delete_cart_in.book_id))
    try:
        if books[0].quantity <= delete_cart_in.quantity:
            books[0].delete()
        else:
            books[0].quantity -= delete_cart_in.quantity
            books[0].save()
    except IndexError:
        return status.HTTP_404_NOT_FOUND, {'detail': 'book not in cart'}

    return status.HTTP_200_OK, {'detail': 'book deleted from cart'}



