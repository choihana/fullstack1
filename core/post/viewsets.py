from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer


# 게시물의 생성과 조회를 담당하며, 인증된 사용자만 접근 할 수 있음
# 모든 게시물 조회: get_queryset
# 특정 게시물 조회: get_object
# 게시물 생성: create
class PostViewSet(AbstractViewSet):
    http_method_names = ('post','get')
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    #모든 게시물을 반환
    def get_queryset(self):
        return Post.objects.all()

    #특정 게시물 반환
    def get_object(self):
        obj = Post.objects.get_object_by_public_id(
            self.kwargs['pk']
        )
        self.check_object_permissions(self.request, obj)
        return obj

    # 새로운 게시물 생성
    def create(self, request, *args, **kwargs):
        # 클라이언트에서 전달된 데이터를 기반으로 시리얼라이저를 생성
        serializer = self.get_serializer(data = request.data)
        # 시리얼라이저의 유효성 검사
        serializer.is_valid(raise_exception=True)
        # 실제로 데이터를 생성
        self.perform_create(serializer)
        # 생성된 데이터를 응답으로 반환
        return Response(serializer.data, status = status.HTTP_201_CREATED)
