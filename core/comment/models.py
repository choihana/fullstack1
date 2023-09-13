from django.db import models
from core.abstract.models import AbstractModel, AbstractManager
from core.post.models import Post


# Create your models here.

class CommentManager(AbstractManager):
    pass


class Comment(AbstractModel):
    # 연결된 객체가 삭제될때 삭제를 막음 (댓글달린 글은 삭제 막음)
    post = models.ForeignKey("core_post.Post",on_delete=models.PROTECT )
    author = models.ForeignKey("core_user.User", on_delete=models.PROTECT)
    body = models.TextField()
    edited = models.BooleanField(default=False)
    objects = CommentManager()

    def __str__(self):
        return self.author.name

