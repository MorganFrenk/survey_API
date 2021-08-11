"""app_survey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from app_survey.views import (
    SurveyViewSet,
    QuestionViewSet,
    ChoiceViewSet,
    AnswerViewSet,
)


survey_list = SurveyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
survey_detail = SurveyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

question_list = QuestionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
question_detail = QuestionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

choice_list = ChoiceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
choice_detail = ChoiceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

answer_list = AnswerViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
answer_detail = AnswerViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('API/surveys/', survey_list, name='survey-list'),
    path('API/surveys/<int:pk>/', survey_detail, name='survey-detail'),
    path('API/questions/', question_list, name='question-list'),
    path('API/questions<int:pk>/', question_detail, name='question-detail'),
    path('API/choices/', choice_list, name='choice-list'),
    path('API/choices/<int:pk>/', choice_detail, name='choice-detail'),
    path('API/answers/', answer_list, name='answer-list'),
    path('API/answers/<int:pk>/', answer_detail, name='answer-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
