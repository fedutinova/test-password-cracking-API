from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class PasswordCrackingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_crack_md5_hash_success(self):
        url = reverse('cracking:crack_md5_hash')
        data = {"md5_hash": "0cc175b9c0f1b6a831c399e269772661"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Password has been cracked successfully!', response.data['message'])
        self.assertEqual(response.data['cracked_password'], 'a')

    def test_authentication_required(self):
        self.client.logout()
        url = reverse('cracking:crack_md5_hash')
        response = self.client.post(url, {'md5_hash': 'd41d8cd98f00b204e9800998ecf8427e'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crack_md5_hash_failure(self):
        url = reverse('cracking:crack_md5_hash')
        data = {"md5_hash": "ffffffffffffffffffffffffffffffff"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Failed to crack the password.', response.data['message'])

    def test_crack_history(self):
        url = reverse('cracking:crack_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for attempt in response.data:
            self.assertIn('md5_hash', attempt)
            self.assertIn('cracked_password', attempt)
            self.assertIn('is_cracked', attempt)
            self.assertIn('submitted_at', attempt)
            self.assertIn('user', attempt)
