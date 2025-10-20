
from rest_framework.test import APITestCase
from django.urls import reverse
from catalog.models import Product
from users.models import User


class ProductTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@test.com", password="123321")
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(
            name="Test product",
            model="XXX",
            description="The best product",
            price=999.99,
            owner=self.user,
        )

    def test_product_retrieve(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], "Test product")





