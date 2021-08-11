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
        statistics_data = {'Answers number': count}
        return Response(statistics_data)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(survey=self.kwargs['survey_pk'])


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return Choice.objects.filter(question=self.kwargs['question_pk'])


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
