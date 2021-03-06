from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Survey(models.Model):
    user_id = models.ForeignKey(
        User,
        editable=False,
        related_name='created_survey',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    date = models.DateTimeField(editable=False, default=timezone.now)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    user_id = models.ForeignKey(
        User,
        editable=False,
        related_name='questions',
        on_delete=models.CASCADE,
    )
    survey = models.ForeignKey(
        Survey,
        editable=False,
        related_name='questions',
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Choice(models.Model):
    user_id = models.ForeignKey(
        User,
        editable=False,
        related_name='choices',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        editable=False,
        related_name='choices',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user_id = models.ForeignKey(
        User,
        editable=False,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        editable=False,
        default=timezone.now,
    )
    survey = models.ForeignKey(
        Survey,
        editable=False,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        editable=False,
        related_name='answers',
        on_delete=models.CASCADE,
    )
    choice = models.ForeignKey(
        Choice,
        related_name='answers',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.choice.text
