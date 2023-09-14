from django.shortcuts import render

from core.abstract.viewsets import AbstractViewSet
from core.auth.permissions import UserPermission
from core.comment.serializers import CommentSerializer


# Create your views here.

class CommentViewSet(AbstractViewSet):
    http_method_names =  ('post','get','put','delete')
    permission_classes = (UserPermission,)
    serializer_class = CommentSerializer
