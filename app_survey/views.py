from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from app_survey.models import Answer, Choice, Question, Survey
from app_survey.serializers import (
    SurveySerializer,
    QuestionSerializer,
    ChoiceSerializer,
    AnswerSerializer,
)


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    @action(detail=True)
    def statistics(self, request, pk=None, renderer_classes=[JSONRenderer]):
        count = Answer.objects.filter(
            survey=Survey.objects.filter(id=pk).get()
        ).count()
        return Response(count)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
