import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from app_survey.models import Survey


class SurveysTestCase(APITestCase):

    list_url = reverse('survey-list')

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.survey = Survey.objects.create(
            user_id=self.user,
            name='name',
            description='description',
        )
        self.random_user = User.objects.create_user(
            username='randomuser',
            password='randompass',
        )

    def test_surveys_list_authed(self):
        response = self.client.get(self.list_url)
        assert response.status_code == status.HTTP_200_OK

    def test_survey_create_authed(self):
        response = self.client.post(
            self.list_url,
            data={
                'name': 'title',
                'description': 'description',
            },
            format='json',
        )
        new_survey = Survey.objects.filter(name='title').get()
        expected_json = {
            'id': new_survey.id,
            'name': new_survey.name,
            'date': new_survey.date.isoformat()[:-6]+'Z',
            'description': new_survey.description,
            'user_id': new_survey.user_id.id,
        }
        assert response.status_code == status.HTTP_201_CREATED
        assert json.loads(response.content) == expected_json

    def test_survey_create_unauthed(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.list_url,
            data={
                'name': 'name',
                'description': 'description',
            },
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_survey_detail(self):
        response = self.client.get(f'{self.list_url}{self.survey.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_survey_update_owner(self):
        response = self.client.put(
            f'{self.list_url}{self.survey.id}/',
            data={
                'name': 'newname',
                'description': 'newdescription',
            },
            format='json',
        )
        expected_json = {
            'id': self.survey.id,
            'name': 'newname',
            'date': self.survey.date.isoformat()[:-6]+'Z',
            'description': 'newdescription',
            'user_id': self.survey.user_id.id,
        }
        assert json.loads(response.content) == expected_json

    def test_survey_update_random_use(self):
        self.client.force_authenticate(user=self.random_user)
        response = self.client.put(
            f'{self.list_url}{self.survey.id}/',
            data={
                'name': 'newname',
                'description': 'newdescription',
            },
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_survey_delete_owner(self):
        response = self.client.delete(
            f'{self.list_url}{self.survey.id}/',
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Survey.objects.filter(name='name').first()

    def test_survey_delete_random_user(self):
        self.client.force_authenticate(user=self.random_user)
        response = self.client.delete(
            f'{self.list_url}{self.survey.id}/',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
