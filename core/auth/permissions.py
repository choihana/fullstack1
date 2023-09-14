from rest_framework.permissions import BasePermission, SAFE_METHODS

# SAFE_METHOD = (GET, OPTION, HEAD)
class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        if view.basename in ['post']:
            return bool(request.user and
                        request.user.is_authenticated)
        if view.basename in ['post-comment']:
            if request.method in ['DELETE']:
                #운영자거나, 글 혹은 댓글 작성자일 경우 삭제 가능
                return bool(request.user.is_superuser or request.user in [obj.author, obj.post.author])
            return bool(request.user and request.user.is_authenticated)
        return False

    def has_permission(self, request, view):
        if view.basename in ['post',"post-comment"]:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS
            return bool(request.user and
                        request.user.is_authenticated)
        return False