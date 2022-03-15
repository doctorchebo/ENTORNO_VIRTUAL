from django.apps import AppConfig


class CustodiaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custodia'

    def ready(self):
        import custodia.signals
