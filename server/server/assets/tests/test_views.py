import uuid

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from server.assets.models import Asset, AssetClass, Exchange
from server.assets.tests.factories import (AssetClassFactory, AssetFactory,
                                           ExchangeFactory)
from server.users.tests.factories import AdminFactory, UserFactory


class ExchangeViewTests(APITestCase):

    def setUp(self):
        self.admin = AdminFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin.auth_token.key
        )
        self.exchange = ExchangeFactory(
            name="Exchange"
        )
        self.data = {
            'name': 'Exchange Name',
            'alt_name': 'Exchange Alt Name',
            'is_active': True
        }

    def test_list_exchanges(self):
        """Admins can list exchanges."""
        response = self.client.get(reverse("v1:exchanges-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_exchanges(self):
        """Admins can create exchanges."""
        response = self.client.post(reverse("v1:exchanges-list"), self.data)
        exchange = Exchange.objects.filter(name=self.data["name"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exchange.exists())

        exchange = exchange.first()
        self.assertEqual(exchange.name, self.data['name'])
        self.assertEqual(exchange.alt_name, self.data['alt_name'])
        self.assertEqual(exchange.is_active, self.data['is_active'])

    def test_create_exchange_invalid(self):
        """Users cannot create exchanges."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        response = self.client.post(reverse("v1:exchanges-list"), self.data)
        exchange = Exchange.objects.filter(name=self.data["name"])

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(exchange.exists())

    def test_partial_update_exchanges(self):
        """Admins can partially update exchanges."""
        data = {"name": "New Exchange Name"}

        response = self.client.patch(
            reverse("v1:exchanges-detail", args=[self.exchange.pk]),
            data
        )
        self.exchange.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.exchange.name, data["name"])

    def test_partial_update_exchanges_invalid(self):
        """Users can not partially update exchanges."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        data = {"name": "New Exchange Name"}

        response = self.client.patch(
            reverse("v1:exchanges-detail", args=[self.exchange.pk]),
            data
        )
        self.exchange.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.exchange.name, "Exchange")

    def test_delete_exchanges(self):
        """Admins can delete exchanges."""
        response = self.client.delete(
            reverse("v1:exchanges-detail", args=[self.exchange.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Exchange.objects.filter(pk=self.exchange.pk).exists()
        )

    def test_delete_exchanges_invalid(self):
        """Users can not delete exchanges."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:exchanges-detail", args=[self.exchange.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Exchange.objects.filter(pk=self.exchange.pk).exists()
        )


class AssetClassViewTests(APITestCase):

    def setUp(self):
        self.admin = AdminFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin.auth_token.key
        )
        self.asset_class = AssetClassFactory(
            name="Asset Class"
        )
        self.data = {
            'name': 'Asset Class Name',
            'alt_name': 'Asset Class Alt Name',
            'is_active': True
        }

    def test_admin_list_asset_class(self):
        """Asset class are listed for admins."""
        response = self.client.get(reverse("v1:assetclasses-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_list_asset_class(self):
        """Asset class are listed for users."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        response = self.client.get(reverse("v1:assetclasses-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_asset_class(self):
        """Asset class can be created by admins."""
        response = self.client.post(reverse("v1:assetclasses-list"), self.data)
        asset_class = AssetClass.objects.filter(name=self.data["name"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(asset_class.exists())

        asset_class = asset_class.first()
        self.assertEqual(asset_class.name, self.data['name'])
        self.assertEqual(asset_class.alt_name, self.data['alt_name'])
        self.assertEqual(asset_class.is_active, self.data['is_active'])

    def test_create_asset_class_invalid(self):
        """Asset class can not be created by users."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        response = self.client.post(reverse("v1:assetclasses-list"), self.data)
        asset_class = AssetClass.objects.filter(name=self.data["name"])

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(asset_class.exists())

    def test_partial_update_asset_class(self):
        """Asset class can be partially updated by admins."""
        data = {"name": "New Asset Class Name"}

        response = self.client.patch(
            reverse("v1:assetclasses-detail", args=[self.asset_class.pk]),
            data
        )
        self.asset_class.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.asset_class.name, data["name"])

    def test_partial_update_asset_class_invalid(self):
        """Asset class can not be partially updated by users."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        data = {"name": "New Asset Class Name"}

        response = self.client.patch(
            reverse("v1:assetclasses-detail", args=[self.asset_class.pk]),
            data
        )
        self.asset_class.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.asset_class.name, "Asset Class")

    def test_delete_asset_class(self):
        """Asset class can be deleted by admins."""
        response = self.client.delete(
            reverse("v1:assetclasses-detail", args=[self.asset_class.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            AssetClass.objects.filter(pk=self.asset_class.pk).exists()
        )

    def test_delete_asset_class_invalid(self):
        """Asset class can not be deleted by users."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:assetclasses-detail", args=[self.asset_class.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            AssetClass.objects.filter(pk=self.asset_class.pk).exists()
        )


class AssetViewTests(APITestCase):

    def setUp(self):
        self.admin = AdminFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.admin.auth_token.key
        )
        self.exchange = ExchangeFactory()
        self.asset_class = AssetClassFactory()
        self.asset = AssetFactory(
            name="Asset",
            exchange=self.exchange,
            asset_class=self.asset_class
        )
        self.data = {
            'id': str(uuid.uuid4()),
            'name': 'Asset Name',
            'asset_class': self.asset_class.name,
            'easy_to_borrow': True,
            'exchange': self.exchange.name,
            'marginable': True,
            'shortable': True,
            'status': Asset.ACTIVE,
            'symbol': 'SYMBOL',
            'tradable': True,
        }

    def test_list_assets_admin(self):
        """Assets are listed for admins."""
        response = self.client.get(reverse("v1:assets-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_assets_user(self):
        """Assets are listed for users."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        response = self.client.get(reverse("v1:assets-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_asset(self):
        """Assets can be created by admins."""
        response = self.client.post(reverse("v1:assets-list"), self.data)
        asset = Asset.objects.filter(id=self.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(asset.exists())

        asset = asset.first()
        self.assertEqual(asset.name, self.data['name'])
        self.assertEqual(asset.asset_class.name, self.data['asset_class'])
        self.assertEqual(asset.easy_to_borrow, self.data['easy_to_borrow'])
        self.assertEqual(asset.exchange.name, self.data['exchange'])
        self.assertEqual(asset.marginable, self.data['marginable'])
        self.assertEqual(asset.shortable, self.data['shortable'])
        self.assertEqual(asset.status, self.data['status'])
        self.assertEqual(asset.symbol, self.data['symbol'])
        self.assertEqual(asset.tradable, self.data['tradable'])

    def test_create_asset_invalid(self):
        """Assets can not be created by users."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        response = self.client.post(reverse("v1:assets-list"), self.data)
        asset = Asset.objects.filter(id=self.data["id"])

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(asset.exists())

    def test_asset_partial_update(self):
        """Assets can be partially updated by admins."""
        data = {"name": "New Name"}

        response = self.client.patch(
            reverse("v1:assets-detail", args=[self.asset.pk]),
            data
        )
        self.asset.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.asset.name, data["name"])

    def test_asset_partial_update_asset_class(self):
        """Assets can asset class updated by admins."""
        new_asset_class = AssetClassFactory()
        data = {"asset_class": new_asset_class.name}

        response = self.client.patch(
            reverse("v1:assets-detail", args=[self.asset.pk]),
            data
        )
        self.asset.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.asset.asset_class.name, data["asset_class"])

    def test_asset_partial_update_exchange(self):
        """Assets can have exchange updated by admins."""
        new_exchange = ExchangeFactory()
        data = {"exchange": new_exchange.name}

        response = self.client.patch(
            reverse("v1:assets-detail", args=[self.asset.pk]),
            data
        )
        self.asset.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.asset.exchange.name, data["exchange"])

    def test_asset_partial_update_invalid(self):
        """Assets can not be partially updated by users."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        data = {"name": "New Name"}

        response = self.client.patch(
            reverse("v1:assets-detail", args=[self.asset.pk]),
            data
        )
        self.asset.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.asset.name, "Asset")

    def test_delete_asset(self):
        """Assets can be deleted by admins."""
        response = self.client.delete(
            reverse("v1:assets-detail", args=[self.asset.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Asset.objects.filter(pk=self.asset.pk).exists())

    def test_delete_asset_invalid(self):
        """Assets can not be deleted by users."""
        user = UserFactory()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + user.auth_token.key
        )
        response = self.client.delete(
            reverse("v1:assets-detail", args=[self.asset.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Asset.objects.filter(pk=self.asset.pk).exists())