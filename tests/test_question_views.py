import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from app_survey.models import Question, Survey


class QuestionsTestCase(APITestCase):

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
        self.random_user = User.objects.create_user(
            username='randomuser',
            password='randompass',
        )
        self.questions_url = f'{reverse("survey-list")}{self.survey.id}/questions/'
        
    def test_questions_list_authed(self):
        response = self.client.get(self.questions_url)
        assert response.status_code == status.HTTP_200_OK
        assert 'q-text' in json.loads(response.content)[0]['text']

    def test_question_create_authed(self):
        response = self.client.post(
            self.questions_url,
            data={
                'text': 'new-q-text',
            },
            format='json',
        )
        new_question = Question.objects.filter(text='new-q-text').get()
        expected_json = {
            'id': new_question.id,
            'text': new_question.text,
            'user_id': new_question.user_id.id,
            'survey': new_question.survey_id,
        }
        assert response.status_code == status.HTTP_201_CREATED
        assert json.loads(response.content) == expected_json

    def test_question_create_unauthed(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.questions_url,
            data={
                'text': 'new-q-text',
            },
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

