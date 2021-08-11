from rest_framework import serializers

from app_survey.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'creator_user_id', 'name', 'date', 'description']
