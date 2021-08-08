from django.contrib import admin

from .models import Answer, Survey


admin.site.register(Survey)
admin.site.register(Answer)
