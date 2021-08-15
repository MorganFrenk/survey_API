import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from app_survey.models import Answer, Choice, Question, Survey


class AnswersTestCase(APITestCase):

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
        self.answer = Answer.objects.create(
            user_id=self.user,
            survey=self.survey,
            question_id=self.question.id,
            choice=self.choice,
        )
        self.random_user = User.objects.create_user(
            username='randomuser',
            password='randompass',
        )
        self.answers_list_url = (
            f'{reverse("survey-list")}'
            + f'{self.survey.id}/questions/'
            + f'{self.question.id}/answers/'
        )
        self.answers_detail_url = f'{self.answers_list_url}{self.answer.id}/'

    def test_answers_list_authed(self):
        response = self.client.get(self.answers_list_url)
        assert response.status_code == status.HTTP_200_OK
        assert self.choice.id == json.loads(response.content)[0]['choice']

    def test_answer_create_authed(self):
        response = self.client.post(
            self.answers_list_url,
            data={
                'choice': self.choice.id,
            },
            format='json',
        )
        new_answer = Answer.objects.filter(id=2).get()
        expected_json = {
            'id': new_answer.id,
            'user_id': new_answer.user_id.id,
            'survey': new_answer.survey.id,
            'question': new_answer.question.id,
            'choice': new_answer.choice.id,
            'date': new_answer.date.isoformat()[:-6]+'Z',
        }
        assert response.status_code == status.HTTP_201_CREATED
        assert json.loads(response.content) == expected_json

    def test_answer_create_unauthed(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(
            self.answers_list_url,
            data={
                'choice': self.choice.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_answer_detail(self):
        response = self.client.get(self.answers_list_url)
        assert response.status_code == status.HTTP_200_OK

    def test_answer_update_owner(self):
        new_choice = Choice.objects.create(
            text='new-choice-text',
            user_id=self.user,
            question_id=self.question.id,
        )
        response = self.client.put(
            self.answers_detail_url,
            data={
                'choice': new_choice.id,
            },
            format='json',
        )
        expected_json = {
            'id': self.answer.id,
            'user_id': self.answer.user_id.id,
            'survey': self.answer.survey.id,
            'question': self.answer.question.id,
            'choice': new_choice.id,
            'date': self.answer.date.isoformat()[:-6]+'Z',
        }
        assert response.status_code == status.HTTP_200_OK
        assert json.loads(response.content) == expected_json

    def test_answer_update_random_user(self):
        self.client.force_authenticate(user=self.random_user)
        new_choice = Choice.objects.create(
            text='new-choice-text',
            user_id=self.user,
            question_id=self.question.id,
        )
        response = self.client.put(
            self.answers_detail_url,
            data={
                'choice': new_choice.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_answer_delete_owner(self):
        response = self.client.delete(
            self.answers_detail_url,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Answer.objects.filter(choice=self.choice).first()

    def test_answer_delete_random_user(self):
        self.client.force_authenticate(user=self.random_user)
        response = self.client.delete(
            self.answers_detail_url,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_answer_not_survey_owner(self):
        self.client.force_authenticate(user=self.random_user)
        response = self.client.post(
            self.answers_list_url,
            data={
                'choice': self.choice.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
