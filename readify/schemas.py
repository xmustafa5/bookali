from ninja import Schema
from pydantic import EmailStr


class Book(Schema):
    id: int
    name: str
    image: str
    author: str
    date: str
    rate: float


class BooksOut(Schema):
    books: list[Book]


class BookOut(Book):
    description: str
    price: str


class Category(Schema):
    name: str


class BookCategory(Schema):
    id: int
    name: str
    image: str
    author: str
    date: str
    rate: float
    category: Category


class CategoryBookOut(Schema):
    category: str
    books: list[BookCategory]


class OrderOut(Schema):
    user: str
    book: str
    address: str
    extra_info: str


class CartIn(Schema):
    email: EmailStr
    book_id: int
    quantity: int


class Cart(Schema):
    book: list[Book]


class GetCartOut(Schema):
    book: list[Book]
    total_price: float


class AddressIn(Schema):
    id: int
    city: str
    town: str
    nearby: str
    phone_number: str


class OrderIn(Schema):
    email: EmailStr
    address: AddressIn


class OrderBookIn(OrderIn):
    quantity: int
    book_id: int


class DeleteCartIn(Schema):
    email: EmailStr
    book_id: int
    quantity: int


class AddressOut(Schema):
    address: list[AddressIn]
