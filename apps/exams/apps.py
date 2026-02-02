from django.apps import AppConfig

class ExamsConfig(AppConfig):
    name = 'apps.exams'

    def ready(self):
        import apps.exams.signals