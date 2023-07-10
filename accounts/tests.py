from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.urls import reverse
from .models import User
from .serializers import UserSerializer, RecruiterRegisterSerializer
from django.core.exceptions import ValidationError


class AdminTests(TestCase):
    def test_users(self):
        self.client = Client()
        with self.assertRaises(ValidationError) as cm:

            self.admin_user = User.objects.create_superuser(
                username='admin',
                password='123',
                email='fda@gmail.com'
            )
            self.client.force_login(self.admin_user)
            self.user = User.objects.create(
                username='mantis',
                password='123',
                email='111'
            )
            self.user1 = User.objects.create(
                username='Mantis',
                password='123',
                email='1123'
            )
        the_exception = cm.exception
        # print(the_exception, " setUp")
        # url = reverse('accounts:index')
        # response = self.client.get(url)

        # self.assertEqual(response.status_code, 400)

    def test_user_case_insensitive(self):
        with self.assertRaises(ValidationError) as cm:
            user = User.objects.create(
                username='hantis',
                password='123',
                email='ascker@gmail.com'
            )
            # user.clean()
            # with self.assertRaises(ValidationError) as ctx:
            #     user.save()
            # print(ctx.exception)
            user2 = User.objects.create(
                username='Hantis',
                password='123',
                email='ascker@gmail.com'
            )
        the_exception = cm.exception
        # url = reverse('accounts:index')
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, 400)

        # print(the_exception, "usercase insensitive")

        # self.assertEqual(the_exception.error_code, 3)
    def test_if_password_is_hashed(self):
        password = 'newpassword'
        # with self.assertRaises(ValidationError) as cm:
        user = User(
            username='NewUser',
            password=password,
            email='someuser@gmail.com'
        )
        # print(user.password)

        user.set_password(password)
        user.save()
        # the_exception = cm.exception
        # url = reverse('accounts:index')
        # response = self.client.get(url)
        hashedpassword = user.password
        # print(hashedpassword)
        self.assertNotEqual(hashedpassword, password)

        # print("usercase insensitive")

        # self.assertEqual(the_exception.error_code, 3)

    def test_userserializer_case_insensitive(self):
        user = None
        user2 = None
        try:
            user = UserSerializer(data={
                'username': 'hantis',
                'password': 'newpassword123',
                'email': 'hacker@gmail.com'}
            )
            user2 = UserSerializer(data={
                'username': 'qAntis',
                'password': 'paswioqadda',
                'email': 'Hacker@gmail.com'}
            )
            user.is_valid(raise_exception=True)
            user2.is_valid(raise_exception=True)
            user.save()
            user2.save()
            # print(user.errors)
            # print(user2.errors)

        except Exception as e:
            # user.is_valid(raise_exception=True)
            # user2.is_valid(raise_exception=True)
            # print(user.error_messages)
            # print(user2.errors)
            # print(e, ' serializer')
            pass
        # user.errors
        # # is_valid(raise_exception=True)
        # user2.is_valid(raise_exception=True)

        # assert user == user2


def test_recruiterserializer(self):
    user = RecruiterRegisterSerializer(data={
        'username': 'hantis',
        'password1': 'newpassword123',
        'password2': 'newpassword123',
        'email': 'hack13245er@gmail.com'}
    )
    user2 = RecruiterRegisterSerializer(data={
        'username': 'sqwersf',
        'password1': 'paswioqadda',
        'password2': 'paswioqadda',
        'email': 'Hac123ker@gmail.com'}
    )
    print(user2.password)

    try:
        user.is_valid(raise_exception=True)
        user2.is_valid(raise_exception=True)
        user.save()
        user2.save()
        print(user2.to_representation())
    except Exception as e:
        # user.is_valid(raise_exception=True)
        # user2.is_valid(raise_exception=True)
        # print(user.error_messages)
        print(user2.errors)
        print(e, ' serializer')

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        pass
        # url = reverse('accounts:index')
        # print(User.objects.all())
        # res = self.client.get(url)
        # self.assertContains(res, self.user.username)
        # self.assertContains(res, self.user.email)
