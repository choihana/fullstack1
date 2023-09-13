from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer


# post 모델을 JSON 형식으로 직렬화하며, 요청된 데이터를 검증하여 유효한 경우만 저장함
# 현재 사용자와 작성자를 비교하여 다른 사용자의 글을 생성하지 못하도록 함

class PostSerializer(AbstractSerializer):

    #유저 모델과의 관계를 나타내고, user의 public_id로 연결됨
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='public_id'
    )
    # author의 유효성 검사
    def validate_author(self, value):
        if self.context['request'].user != value:
            raise ValidationError('You cant create a post for another user.')
        return value

    class Meta:
        model = Post
        fields= [ 'id', 'author','body','edited','created','updated']
        read_only_fields = ['edited']

    #auther 정보(id, username,email등) 를 json으로 다 노출
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(
            rep['author']
        )
        rep['author'] = UserSerializer(author).data
        return rep