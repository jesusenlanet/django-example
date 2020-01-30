import pytest

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from usermanage.models import IbanUser


"""
    Testing data:
    2 Users:
        pk  name
        1   user1
        2   user2
        
    4 iban users
        pk      IBAN                        first_name      last_name   creator
        1       ES0400758872768146768871    user1           user1       1
        2       ES1231904186817934673756    user1           user1       1
        3       ES3104876591071767173958    user2           user2       2
        4       ES4900819163254588566621    user2           user2       2
"""

IBAN_1 = 'ES0400758872768146768871'
IBAN_2 = 'ES1231904186817934673756'
IBAN_3 = 'ES3104876591071767173958'
IBAN_4 = 'ES4900819163254588566621'


USERNAME_1 = 'user1'
USERNAME_2 = 'user2'

NEW_IBAN = 'NL70RABO3518588532'


@pytest.mark.django_db
class IbanUsersTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        for i in range(1, 3):
            user = User.objects.get(pk=i)
            user.set_password(f'user{i}')
            user.save()
            user = authenticate(username=f'user{i}', password=f'user{i}')
            setattr(self, f'user{i}', user)

    def test_list_user1_ok(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertContains(response, IBAN_1)
        self.assertContains(response, IBAN_2)
        self.assertNotContains(response, IBAN_3)
        self.assertNotContains(response, IBAN_4)

    def test_list_user2_ok(self):
        self.client.login(username=USERNAME_2, password=USERNAME_2)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertNotContains(response, IBAN_1)
        self.assertNotContains(response, IBAN_2)
        self.assertContains(response, IBAN_3)
        self.assertContains(response, IBAN_4)

    def test_get_detail_ok(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        response = self.client.get(reverse('user-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_detail_unauthorized(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        response = self.client.get(reverse('user-detail', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_get_detail_not_found(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        response = self.client.get(reverse('user-detail', kwargs={'pk': 42}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_create_ok(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        len_users_pre = IbanUser.objects.count()
        data = {
            'iban': NEW_IBAN,
            'first_name': 'test user',
            'last_name': 'something'
        }
        response = self.client.post(reverse('user-list'), data=data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        len_users_post = IbanUser.objects.count()
        self.assertLess(len_users_pre, len_users_post)

    def test_create_ko_iban_fail(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        len_users_pre = IbanUser.objects.count()
        data = {
            'iban': 'foo',
            'first_name': 'test user',
            'last_name': 'something'
        }
        response = self.client.post(reverse('user-list'), data=data)
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)
        len_users_post = IbanUser.objects.count()
        self.assertEqual(len_users_pre, len_users_post)

    def test_create_ko_first_name_non_existent_fail(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        len_users_pre = IbanUser.objects.count()
        data = {
            'iban': NEW_IBAN,
            'last_name': 'something'
        }
        response = self.client.post(reverse('user-list'), data=data)
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)
        len_users_post = IbanUser.objects.count()
        self.assertEqual(len_users_pre, len_users_post)

    def test_create_ko_first_name_empty_string_fail(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        len_users_pre = IbanUser.objects.count()
        data = {
            'iban': NEW_IBAN,
            'first_name': '',
            'last_name': 'something'
        }
        response = self.client.post(reverse('user-list'), data=data)
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)
        len_users_post = IbanUser.objects.count()
        self.assertEqual(len_users_pre, len_users_post)

    def test_create_ko_last_name_non_existent_fail(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        len_users_pre = IbanUser.objects.count()
        data = {
            'iban': NEW_IBAN,
            'first_name': 'something'
        }
        response = self.client.post(reverse('user-list'), data=data)
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)
        len_users_post = IbanUser.objects.count()
        self.assertEqual(len_users_pre, len_users_post)

    def test_create_ko_last_name_empty_string_fail(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        len_users_pre = IbanUser.objects.count()
        data = {
            'iban': NEW_IBAN,
            'first_name': 'something',
            'last_name': ''
        }
        response = self.client.post(reverse('user-list'), data=data)
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)
        len_users_post = IbanUser.objects.count()
        self.assertEqual(len_users_pre, len_users_post)

    def test_delete_ok(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        len_users_pre = IbanUser.objects.count()
        response = self.client.post(reverse('user-delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        len_users_post = IbanUser.objects.count()
        self.assertGreater(len_users_pre, len_users_post)

    def test_delete_unauthorized(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        len_users_pre = IbanUser.objects.count()
        response = self.client.post(reverse('user-delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        len_users_post = IbanUser.objects.count()
        self.assertEqual(len_users_pre, len_users_post)

    def test_delete_not_found(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        response = self.client.post(reverse('user-delete', kwargs={'pk': 42}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_update_ok(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        iban_user = IbanUser.objects.filter(creator=self.user1).first()

        data = {
            'iban': NEW_IBAN,
            'first_name': 'updated_first_name',
            'last_name': 'updated_last_name',
        }

        response = self.client.post(reverse('user-detail', kwargs={'pk': iban_user.pk}), data=data)
        self.assertEqual(response.status_code, HTTP_200_OK)

        iban_user.refresh_from_db()
        self.assertEqual(iban_user.iban, NEW_IBAN)
        self.assertEqual(iban_user.first_name, 'updated_first_name')
        self.assertEqual(iban_user.last_name, 'updated_last_name')

    def test_update_ko_non_owned_user(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        iban_user = IbanUser.objects.filter(creator=self.user2).first()

        data = {
            'iban': NEW_IBAN,
            'first_name': 'updated_first_name',
            'last_name': 'updated_last_name',
        }

        response = self.client.post(reverse('user-detail', kwargs={'pk': iban_user.pk}), data=data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

        iban_user.refresh_from_db()
        self.assertEqual(iban_user.iban, IBAN_3)
        self.assertEqual(iban_user.first_name, USERNAME_2)
        self.assertEqual(iban_user.last_name, USERNAME_2)

    def test_update_ko_non_existing_user(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        data = {
            'iban': NEW_IBAN,
            'first_name': 'updated_first_name',
            'last_name': 'updated_last_name',
        }
        response = self.client.post(reverse('user-detail', kwargs={'pk': 42}), data=data)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_update_ko_iban_fail(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        iban_user = IbanUser.objects.filter(creator=self.user1).first()

        data = {
            'iban': 'foo',
            'first_name': 'updated_first_name',
            'last_name': 'updated_last_name',
        }

        response = self.client.post(reverse('user-detail', kwargs={'pk': iban_user.pk}), data=data)
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)

        iban_user.refresh_from_db()
        self.assertEqual(iban_user.iban, IBAN_1)
        self.assertEqual(iban_user.first_name, USERNAME_1)
        self.assertEqual(iban_user.last_name, USERNAME_1)

    def test_update_ko_first_name_fail(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        iban_user = IbanUser.objects.filter(creator=self.user1).first()

        data = {
            'iban': iban_user.iban,
            'first_name': '',
            'last_name': 'updated_last_name',
        }

        response = self.client.post(reverse('user-detail', kwargs={'pk': iban_user.pk}), data=data)
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)

        iban_user.refresh_from_db()
        self.assertEqual(iban_user.iban, IBAN_1)
        self.assertEqual(iban_user.first_name, USERNAME_1)
        self.assertEqual(iban_user.last_name, USERNAME_1)

    def test_update_ko_last_name_fail(self):
        self.client.login(username=USERNAME_1, password=USERNAME_1)
        iban_user = IbanUser.objects.filter(creator=self.user1).first()

        data = {
            'iban': iban_user.iban,
            'first_name': 'foo',
            'last_name': '',
        }

        response = self.client.post(reverse('user-detail', kwargs={'pk': iban_user.pk}), data=data)
        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)

        iban_user.refresh_from_db()
        self.assertEqual(iban_user.iban, IBAN_1)
        self.assertEqual(iban_user.first_name, USERNAME_1)
        self.assertEqual(iban_user.last_name, USERNAME_1)
