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
from django.urls import include, path
from rest_framework_nested import routers

from app_survey.views import (AnswerViewSet, ChoiceViewSet, QuestionViewSet,
                              SurveyViewSet)


router = routers.SimpleRouter()
router.register(r'surveys', SurveyViewSet)

survey_router = routers.NestedSimpleRouter(
    router,
    r'surveys',
    lookup='survey',
)
survey_router.register(
    r'questions',
    QuestionViewSet,
    basename='questions',
)

choices_router = routers.NestedSimpleRouter(
    survey_router,
    r'questions',
    lookup='question',
)
choices_router.register(r'choices', ChoiceViewSet, basename='choices')

answer_router = routers.NestedSimpleRouter(
    survey_router,
    r'questions',
    lookup='question',
)
answer_router.register(r'answers', AnswerViewSet, basename='answers')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(survey_router.urls)),
    path('', include(choices_router.urls)),
    path('', include(answer_router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
