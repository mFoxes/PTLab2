from django.test import TestCase, Client, RequestFactory
from shop.views import PurchaseCreate
from shop.models import Product, Purchase

factory = RequestFactory()

class IndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        painting = Product.objects.create(name="Картина", price=100000, amount=5)
        self.painting_id = painting.id

        statue = Product.objects.create(name="Статуя", price=90000000, amount=1)
        self.statue_id = statue.id

        self.request_data_statue = {
            "product": self.statue_id,
            "person": "Valera",
            "address": "Volgograd"
        }

        self.request_data_painting = {
            "product": self.painting_id,
            "person": "Ivan",
            "address": "Moscow"
        }

    def tearDown(self):
        Product.objects.all().delete()
        Purchase.objects.all().delete()

    def test_purchase(self):
        request = factory.post(f"/buy/{self.statue_id}", data=self.request_data_statue)
        response = PurchaseCreate.as_view()(request)

        self.assertEqual(response.status_code, 200)

        statue = Product.objects.get(name="Статуя")
        self.assertEqual(statue.amount, 0)

        response = self.client.get('/')
        self.assertTrue("Нет в наличии" in response.content.decode())

    def test_multiple_purchase(self):
        request = factory.post(f"/buy/{self.painting_id}", data=self.request_data_painting)
        for i in range(4):
            PurchaseCreate.as_view()(request)

        painting = Product.objects.get(name="Картина")
        self.assertEqual(painting.amount, 1)
