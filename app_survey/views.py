from rest_framework import viewsets

from app_survey.models import Survey
from app_survey.serializers import SurveySerializer


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
