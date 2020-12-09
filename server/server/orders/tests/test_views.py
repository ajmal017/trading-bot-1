import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from server.assets.models import Asset
from server.assets.tests.factories import AssetFactory
from server.orders.models import Order
from server.users.tests.factories import AdminFactory, UserFactory

from .factories import OrderFactory, StopLossFactory, TakeProfitFactory


class OrderViewTests(APITestCase):

    def setUp(self):
        self.admin = AdminFactory()
        self.user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin.auth_token.key
        )
        self.stop_loss = StopLossFactory(
            stop_price=100.50,
            limit_price=110.30
        )
        self.take_profit = TakeProfitFactory(
            limit_price=110.30
        )
        self.order = OrderFactory()

    def test_list_orders(self):
        """Admins can list orders."""
        response = self.client.get(reverse("v1:orders-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_order(self):
        """Admins and users can create orders."""
        asset = AssetFactory(symbol="AAPL")
        order_1 = {
            "status": "open",
            "symbol": "AAPL",
            "quantity": 100.05,
            "side": "buy",
            "type": "market",
            "time_in_force": "day",
            "client_order_id": str(uuid.uuid4())
        }
        order_2 = {
            "status": "open",
            "symbol": "AAPL",
            "quantity": 100.05,
            "side": "sell",
            "type": "market",
            "time_in_force": "day",
            "client_order_id": str(uuid.uuid4())
        }

        # Admin create order
        response = self.client.post(reverse("v1:orders-list"), order_1)
        order = Order.objects.filter(client_order_id=order_1["client_order_id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(order.exists())

        # User create order
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )
        response = self.client.post(reverse("v1:orders-list"), order_2)
        order = Order.objects.filter(client_order_id=order_2["client_order_id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(order.exists())

    def test_create_order_invalid(self):
        """Incorrect orders raise validations errors."""
        # TO DO
        self.assertTrue(False)

    def test_partial_update_order(self):
        """Admins and users can partially update orders."""
        AssetFactory(symbol="ADMIN SYMBOL")
        AssetFactory(symbol="USER SYMBOL")
        order_1 = {
            "symbol": "ADMIN SYMBOL"
        }
        order_2 = {
            "symbol": "USER SYMBOL"
        }

        # Admin patch order
        response = self.client.patch(
            reverse("v1:orders-detail", args=[self.order.pk]),
            order_1
        )
        self.order.refresh_from_db()
        asset = self.order.symbol

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(asset.symbol, order_1["symbol"])

        # User patch order
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )
        response = self.client.patch(
            reverse("v1:orders-detail", args=[self.order.pk]),
            order_2
        )
        self.order.refresh_from_db()
        asset = self.order.symbol

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(asset.symbol, order_2["symbol"])

    def test_delete_order(self):
        """Admins can delete orders."""
        response = self.client.delete(
            reverse("v1:orders-detail", args=[self.order.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Order.objects.filter(pk=self.order.pk).exists()
        )

    def test_delete_order_invalid(self):
        """Users can not delete orders."""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:orders-detail", args=[self.order.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Order.objects.filter(pk=self.order.pk).exists()
        )
