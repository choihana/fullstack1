import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from core.abstract.models import AbstractManager, AbstractModel


class UserManager(BaseUserManager,AbstractManager):

    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError('User must have an username.')
        if email is None:
            raise TypeError('User must have an email.')
        if password is None:
            raise TypeError('User must have a Password.')
        user = self.model(username=username,
                          email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        if password is None:
            raise TypeError('Superuser must have a password.')
        if email is None:
            raise TypeError('Superuser must have an email.')
        if username is None:
            raise TypeError('Superuser must have an username.')
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractModel ,AbstractBaseUser, PermissionsMixin):
    #AbstractModel에 있음 , 데이터베이스가 변경되지 않으므로 마이그레이션 할 필요 없음
    #public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    #created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)

    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    ## 좋아요 관련 필드 추가
    posts_liked = models.ManyToManyField(
        'core_post.Post', related_name='liked_by'
    )

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def like(self, post):
        return self.posts_liked.add(post)

    def remove_like(self,post):
        return self.posts_liked.remove(post)

    def has_liked(self,post):
        return self.posts_liked.filter(pk=post.pk).exists()