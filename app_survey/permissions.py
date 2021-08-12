from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_has_permission = (obj.user_id == request.user)

        if obj.__class__.__name__ == 'Survey':
            user_has_permission_for_parent = True

        elif obj.__class__.__name__ == 'Question':
            user_has_permission_for_parent = (
                obj.survey.user_id == request.user,
            )

        elif obj.__class__.__name__ == 'Choice':
            user_has_permission_for_parent = (
                obj.question.user_id == request.user,
            )

        return user_has_permission and user_has_permission_for_parent
