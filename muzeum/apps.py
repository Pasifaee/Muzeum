from django.apps import AppConfig


class MuzeumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'muzeum'

    def ready(self):
        import muzeum.signals