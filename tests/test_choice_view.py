import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from app_survey.models import Choice, Question, Survey


class ChoicesTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.survey = Survey.objects.create(
            user_id=self.user,
            name='survey-name',
            description='description',
        )
        self.question = Question.objects.create(
            text='q-text',
            user_id=self.user,
            survey_id=self.survey.id,
        )
        self.choice = Choice.objects.create(
            text='choice-text',
            user_id=self.user,
            question_id=self.question.id,
        )
        self.random_user = User.objects.create_user(
            username='randomuser',
            password='randompass',
        )
        self.choices_list_url = (
            f'{reverse("survey-list")}'
            + f'{self.survey.id}/questions/'
            + f'{self.question.id}/choices/'
        )
        self.choice_detail_url = f'{self.choices_list_url}{self.choice.id}/'

    def test_choices_list_authed(self):
        response = self.client.get(self.choices_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert 'choice-text' in json.loads(response.content)[0]['text']

    def test_choice_create_authed(self):
        response = self.client.post(
            self.choices_list_url,
            data={
                'text': 'new-choice-text',
            },
            format='json',
        )
        new_choice = Choice.objects.filter(text='new-choice-text').get()
        expected_json = {
            'id': new_choice.id,
            'text': new_choice.text,
            'user_id': new_choice.user_id.id,
            'question': new_choice.question.id,
        }
        assert response.status_code == status.HTTP_201_CREATED
        assert json.loads(response.content) == expected_json

    def test_choice_create_unauthed(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.choices_list_url,
            data={
                'text': 'new-choice-text',
            },
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
