from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Category, Category, MenuItem, Cart

class UserSetUp(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(username='customer', password='strong_password_123')
        self.delivery = User.objects.create_user(username='delivery', password='strong_password_123')
        self.manager = User.objects.create_user(username='manager', password='strong_password_123')

        self.manager_group = Group.objects.create(name='Manager')
        self.delivery_group = Group.objects.create(name='Delivery')
        self.delivery = User.objects.get(username='delivery').groups.add(Group.objects.get(name='Delivery'))
        self.manager = User.objects.get(username='manager').groups.add(Group.objects.get(name='Manager'))


    def get_token(self, username, password):
        url = reverse('token-create')
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        return response.data['auth_token']

class UserTest(APITestCase):

    def test_user_creation(self):
        response = self.client.post(reverse('user-create'), {'username': 'customer', 'password': 'strong_password_123'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('user-create'), {'username': 'customer', 'password': 'strong_password_123'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('user-create'), {'username': '<script>', 'password': 'strong_password_123'})
        self.assertEqual(response.data['username'][0], 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class ManagerGroupTest(UserSetUp):

    def test_manager_group_list_access(self):
        token = self.get_token('manager', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('manager group list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('manager group list'), {'username': 'not_existing_user'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(reverse('manager group list'), {'username': 'customer'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username='customer').groups.values_list('name', flat=True)[0], 'Manager')
        response = self.client.delete(f'/api/groups/manager/users/{User.objects.get(username="customer").id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(f'/api/groups/manager/users/{User.objects.get(username="customer").id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn('Manager', User.objects.get(username='customer').groups.values_list('name', flat=True))

        token = self.get_token('customer', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('manager group list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('manager group list'), {'username': 'not_existing_user'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('manager group list'), {'username': 'customer'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(f'/api/groups/manager/users/{User.objects.get(username="customer").id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        token = self.get_token('delivery', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('manager group list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('manager group list'), {'username': 'not_existing_user'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('manager group list'), {'username': 'customer'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(f'/api/groups/manager/users/{User.objects.get(username="customer").id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeliveryGroupTest(UserSetUp):

    def test_delivery_crew_group_list_access(self):
        token = self.get_token('manager', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('Delivery group list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('Delivery group list'), {'username': 'not_existing_user'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(reverse('Delivery group list'), {'username': 'customer'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username='customer').groups.values_list('name', flat=True)[0], 'Delivery')
        response = self.client.delete(f'/api/groups/delivery-crew/users/{User.objects.get(username="customer").id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(f'/api/groups/delivery-crew/users/{User.objects.get(username="customer").id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotIn('Delivery', User.objects.get(username='customer').groups.values_list('name', flat=True))

        token = self.get_token('customer', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('Delivery group list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('Delivery group list'), {'username': 'not_existing_user'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('Delivery group list'), {'username': 'customer'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(f'/api/groups/delivery-crew/users/{User.objects.get(username="customer").id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        token = self.get_token('delivery', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('Delivery group list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('Delivery group list'), {'username': 'not_existing_user'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(reverse('Delivery group list'), {'username': 'customer'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(f'/api/groups/delivery-crew/users/{User.objects.get(username="customer").id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CategoryTest(UserSetUp):

    def test_category_list_access(self):
        token = self.get_token('manager', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('categories list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = self.get_token('customer', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('categories list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = self.get_token('delivery', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('categories list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_access(self):
        token = self.get_token('manager', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(reverse('categories list'), {'slug': 'test', 'title': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('categories list'), {'slug': 'test', 'title': 'test'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('category', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        token = self.get_token('customer', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('categories list'), {'slug': 'test', 'title': 'test'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(reverse('category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        token = self.get_token('delivery', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(reverse('category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post(reverse('categories list'), {'slug': 'test', 'title': 'test'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(reverse('category', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class MenuItemTest(UserSetUp):

    def setUp(self):

        super().setUp()
        self.category = Category.objects.create(slug='test', title='test')

    def test_menu_item_list_access(self):
        token = self.get_token('manager', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/api/menu-items/', {'title': 'test', 'price': 10, 'featured': False, 'category_id': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/api/menu-items/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete('/api/menu-items/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.post('/api/menu-items/', {'title': 'test', 'price': 10, 'featured': False, 'category_id': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/api/menu-items/', {'title': 'test', 'price': 10, 'featured': False, 'category_id': 20})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        token = self.get_token('customer', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/api/menu-items/', {'title': 'test', 'price': 10, 'featured': False, 'category_id': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/menu-items/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get('/api/menu-items/2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = self.get_token('delivery', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/api/menu-items/', {'title': 'test', 'price': 10, 'featured': False, 'category_id': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/menu-items/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get('/api/menu-items/2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CartTest(UserSetUp):

    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(slug='test', title='test')
        self.menu_item = MenuItem.objects.create(title='test', price=10, featured=False, category=self.category)
        self.menu_item2 = MenuItem.objects.create(title='test2', price=10, featured=False, category=self.category)

    def test_cart_list_access(self):
        token = self.get_token('manager', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/cart/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post('/api/cart/menu-items/', {'menuitem_id': 1, 'quantity': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/cart/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        token = self.get_token('delivery', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/cart/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post('/api/cart/menu-items/', {'menuitem_id': 1, 'quantity': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/cart/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        token = self.get_token('customer', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/cart/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/api/cart/menu-items/', {'menuitem_id': 1, 'quantity': 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/api/cart/menu-items/', {'menuitem_id': 1, 'quantity': 10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post('/api/cart/menu-items/', {'menuitem_id': 2, 'quantity': 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/api/cart/menu-items/')
        self.assertEqual(response.data['count'], 2)
        response = self.client.delete('/api/cart/menu-items/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/cart/menu-items/')
        self.assertEqual(response.data['count'], 0)

class OrderTest(UserSetUp):

    def setUp(self):
        super().setUp()

        self.category = Category.objects.create(slug='test', title='test')
        self.menu_item = MenuItem.objects.create(title='test', price=10, featured=False, category=self.category)
        self.menu_item2 = MenuItem.objects.create(title='test2', price=10, featured=False, category=self.category)
        self.cart = Cart.objects.create(user=User.objects.get(username='customer'), menuitem=self.menu_item, quantity=10, unit_price=10, price=100)
        self.cart = Cart.objects.create(user=User.objects.get(username='customer'), menuitem=self.menu_item2, quantity=10, unit_price=10, price=100)

    def test_order_list_access(self):
        token = self.get_token('customer', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Cart is empty')
        response = self.client.get('/api/orders/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.data['count'], 1)
        response = self.client.delete('/api/orders/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        token = self.get_token('delivery', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/orders/1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.put('/api/orders/1', {'delivery_crew': 1, 'status': 0})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch('/api/orders/1', {'status': 0})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete('/api/orders/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        token = self.get_token('manager', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get('/api/orders/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        delivery_id = User.objects.get(username='delivery').id
        response = self.client.put('/api/orders/1', {'delivery_crew': delivery_id, 'status': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch('/api/orders/1', {'status': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = self.get_token('delivery', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        response = self.client.get('/api/orders/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch('/api/orders/1', {'status': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete('/api/orders/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        token = self.get_token('manager', 'strong_password_123')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.delete('/api/orders/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.data['count'], 0)
