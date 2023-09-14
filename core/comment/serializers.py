from rest_framework import serializers
from core.abstract.serializers import AbstractSerializer
from core.comment.models import Comment
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer


class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset = User.objects.all(), slug_field = 'public_id'
    )
    post = serializers.SlugRelatedField(
        queryset = Post.objects.all(), slug_field = 'public_id'
    )
    def validate_author(self, value):
        if self.context["request"].user != value:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You can't create a post for another user.")
        return value

    #delete, put, patch  요청일 때 수정될 객체를 가진 Instance 속성 제공하며, get/post인경우 none으로 설정됨
    def validate_post(self, value):
        if self.instance:
            return self.instance.post
        return value

    def update(self, instance, validated_date):
        if not instance.edited:
            validated_date['edited'] = True
        instance = super().update(instance, validated_date)
        return instance
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep['author'])
        rep['author'] = UserSerializer(author).data
        return rep

    class Meta:
        model = Comment
        fields = ['id', 'post','author','body','edited','created','updated']
        read_only_fields = ['edited']
