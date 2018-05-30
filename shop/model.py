from datetime import datetime

from pony.orm import Database, Required, Optional, Set, PrimaryKey


db = Database()

class Product(db.Entity):
    """Товар"""
    category = Required('Category')
    title = Required(str)
    description = Optional(str) #будет значение по-умолчанию "пустая строка"
    unit = Optional(int)
    price = Required(float)
    history = Set('ProductHistory')
    amount = Optional(int, default=1)
    # alt_categories = Set('Category')
    # amount = int #сколько товаров в магазине сейчас

class ProductHistory(db.Entity):
    product = Required('Product')
    created = Optional(datetime, default=datetime.now)
    price = Required(float)


class Category(db.Entity):
    """Категория товара"""
    parent = Optional('Category', reverse="children")
    children = Set('Category', reverse="parent")
    title = Required(str)
    products = Set(Product)

class Customer(db.Entity):
    """Покупатель"""
    email = Optional(str)
    phone = Optional(str)
    name = Required(str)
    address = Set('Address')
    cart = Optional('Cart')
    orders = Set('Order')

class Address(db.Entity):
    """Адрес"""
    customer = Required('Customer')
    country = Required(str)
    city = Required(str)
    street = Required(str)
    zip_code = Required(str)
    house = Required(int)

class Cart(db.Entity):
    """Корзина с товарами"""
    customer = Optional('Customer')
    products = Set('CartItem')

class CartItem(Product):
    """Элемент корзины"""
    cart = Required('Cart')

class Order(db.Entity):
    """Заказ"""
    customer = Required('Customer')
    created = Optional(datetime, default=datetime.now)
    products = Set('OrderItem')
    status = Required('Status')

class Status(db.Entity):
    """Статус"""
    name = Required(str)
    orders = Set(Order)

class OrderItem(Product):
    """Товар (одна позиция в заказе)"""
    order = Required('Order')

class Menu:
    """Меню"""

db.bind(provider='sqlite', filename='shop.sqlite', create_db=True)
set_sql_debug(True)
db.generate_mapping(create_tables=True)

with db_session:
    cat = Category(title='Small kitchen appliances')
    prod = Product(category=cat, title='kettle', price=30.5)
    prod = Product(category=cat, title='blender', price=45.5)