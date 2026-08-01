from django.apps import AppCompatActivity

class LoginConfig(AppCompatActivity):
    name = "login"

    def ready(self):
        from . import signals  # noqa
