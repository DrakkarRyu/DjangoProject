from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model



User = get_user_model()


class HelloWorldTestCase(APITestCase):
    def test_hello_world(self):
        response = self.client.get(reverse("posts_home"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostListCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("list_posts")

    def authenticate(self):
        self.client.post(
            reverse("signup"),
            {
                "email": "Rudi@email.com",
                "password": "IamRudi#Luchon",
                "username": "RudiTheHandsome",
            },
        )
        response = self.client.post(
            reverse("login"),
            {
                "email": "Rudi@email.com",
                "password": "IamSuperRudi123",
            },
        )

        token = response.data["tokens"]["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_post_creation(self):
        self.authenticate()
        test_data = {"title": "Test title", "content": "Test content"}
        response = self.client.post(reverse("list_posts"), test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], test_data["title"])