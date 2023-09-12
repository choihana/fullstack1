from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    label = 'core' #애플리케이션의 식별자로 데이터베이스 작업에 사용됨