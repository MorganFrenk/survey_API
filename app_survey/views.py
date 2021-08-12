from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from app_survey.permissions import IsOwnerOrReadOnly
from app_survey.models import Answer, Choice, Question, Survey
from app_survey.serializers import (AnswerSerializer, ChoiceSerializer,
                                    QuestionSerializer, SurveySerializer)


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    @action(detail=True)
    def statistics(self, request, pk=None, renderer_classes=[JSONRenderer]):
        count = Answer.objects.filter(
            survey=Survey.objects.filter(id=pk).get()
        ).count()
        statistics_data = {'Answers number': count}
        return Response(statistics_data)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        obj = Survey.objects.filter(id=self.kwargs['survey_pk']).get()
        self.check_object_permissions(self.request, obj)
        serializer.save(
            user_id=self.request.user,
            survey=Survey.objects.filter(id=self.kwargs['survey_pk']).get()
        )

    def get_queryset(self):
        return Question.objects.filter(survey=self.kwargs['survey_pk'])


class ChoiceViewSet(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        obj = Question.objects.filter(id=self.kwargs['question_pk']).get()
        self.check_object_permissions(self.request, obj)
        serializer.save(user_id=self.request.user)

    def get_queryset(self):
        return Choice.objects.filter(question=self.kwargs['question_pk'])


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get_queryset(self):
        return Answer.objects.filter(question=self.kwargs['question_pk'])
