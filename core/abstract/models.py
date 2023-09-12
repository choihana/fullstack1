import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404

# public_id로 쿼리셋 수행해서 객체 가져와서 반환하는 기능 제공
class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
            return instance
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

class AbstractModel(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = AbstractManager()
    class Meta:
        abstract = True
