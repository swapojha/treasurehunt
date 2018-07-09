from django.apps import AppConfig


class HuntConfig(AppConfig):
    name = 'hunt'
    def ready(self):
        import hunt.signals
