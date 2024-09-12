from django.core.management.base import BaseCommand
from faker import Faker
from LittleLemonAPI.models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Users
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password123',
                email=fake.email()
            )
            print(f"Created user: {user.username}")

        # Create Categories
        for _ in range(5):
            category = Category.objects.create(
                title=fake.word(),
                slug=fake.slug()
            )
            print(f"Created category: {category.title}")

        # Create MenuItems
        categories = Category.objects.all()
        for _ in range(20):
            menu_item = MenuItem.objects.create(
                title=fake.word(),
                price=random.uniform(10.0, 100.0),
                featured=random.choice([True, False]),
                category=random.choice(categories)
            )
            print(f"Created menu item: {menu_item.title}")

        # Create Carts and Orders for random users
        users = User.objects.all()
        menu_items = MenuItem.objects.all()
        for user in users:
            # Add items to cart
            for _ in range(random.randint(1, 5)):
                menu_item = random.choice(menu_items)
                quantity = random.randint(1, 3)
                Cart.objects.create(
                    user=user,
                    menuitem=menu_item,
                    quantity=quantity,
                    price=menu_item.price * quantity,  # Calculate price
                    unit_price=menu_item.price  # Set the unit_price from the menu item price
                )
            print(f"Created cart for user: {user.username}")
            if random.choice([True, False]):
                order = Order.objects.create(
                    user=user,
                    status=random.choice([True, False]),
                    total=random.uniform(50.0, 500.0),
                    date=fake.date_this_year()
                )
                
                # Add items from the cart to the order
                for cart_item in Cart.objects.filter(user=user):
                    # Check if the order item already exists to avoid duplicate entries
                    order_item, created = OrderItem.objects.get_or_create(
                        order=order,
                        menuitem=cart_item.menuitem,
                        defaults={
                            'quantity': cart_item.quantity,
                            'unit_price': cart_item.menuitem.price,
                            'price': cart_item.menuitem.price * cart_item.quantity
                        }
                    )
                    if created:
                        print(f"Created order item for menu item: {cart_item.menuitem.title}")
                    else:
                        print(f"Order item for {cart_item.menuitem.title} already exists in the order")