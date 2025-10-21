from rest_framework import status
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
        url = reverse("product-detail", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test product")

    def test_product_create(self):
        url = reverse('product-list')
        data = {
            "name": "Test product",
            "model":"XXX",
            "description":"The best product",
            "price":999.99,
            "owner":self.user}
        response = self.client.post(url, data)
        product = Product.objects.latest('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(product.price), data["price"])

    def test_product_update(self):
        url = reverse("product-detail", args=(self.product.pk,))
        data = {"name": "Test product_2"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Test product_2")


    def test_product_delete(self):
        url = reverse("product-detail", args=(self.product.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.all().count(), 0)

    def test_product_list(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)



