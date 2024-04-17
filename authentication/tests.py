import logging
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserAccountTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_success(self):
        url = reverse('authorization:signup')  # Ensure you have the correct URL name in urls.py
        data = {"username": "newuser", "password": "newpassword123", "email": "user@example.com"}
        expected_token = "Basic bmV3dXNlcjpuZXdwYXNzd29yZDEyMw=="
        response = self.client.post(url, data, format='json')
        actual_token = response.data['Authorization']
        self.assertEqual(actual_token, expected_token, "The returned authorization token is incorrect.")
        self.assertIn('User registered successfully!', response.data['message'])

    def test_signup_failure(self):
        url = reverse('authorization:signup')
        data = {"username": "newuser"}  # Intentionally missing password to simulate failure
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_verification(self):
        # Assuming there is a user and a token setup
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)
        url = reverse('authorization:test_token')  # Set correct URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Token is valid.')

    def test_get_token_with_creds_success(self):
        url = reverse('authorization:creds')
        username = "user"
        password = "password"
        User.objects.create_user(username=username, password=password)
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Authorization', response.data)

    def test_get_token_with_creds_failure(self):
        url = reverse('authorization:creds')
        data = {'username': 'user'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Both username and password are required.')

