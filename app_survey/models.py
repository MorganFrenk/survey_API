from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    creator_user_id = models.ForeignKey(User, related_name='created_survey')
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user_id = models.ForeignKey(User, related_name='answers')
    survey = models.ForeignKey(Survey, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text
