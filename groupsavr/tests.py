import json
from groupsavr import views
from django.http import HttpRequest
from django.test import TestCase, LiveServerTestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate


class APITests(APITestCase):

    def test_create_feedback(self):
        """
        Ensure we can create a new account object.
        """

        client = APIClient()
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        client.login(username='john', password='johnpassword')

        factory = APIRequestFactory()
        user = User.objects.get(username='john')
        view = views.UserViewSet.as_view({"get":"list"})
        
        request = factory.get('/accounts')
        force_authenticate(request, user=user)
        response = view(request)
        print response.data

        #response = self.client.get('/users/4/')
        #self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})

        #url = '/users'
        #response = self.client.get(url, user=user)
        #print response.__dict__
        #self.assertEqual(response.status_code, 201)
