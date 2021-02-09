from django.apps import AppConfig
from django.contrib import admin


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        self.setup_admin_form()

    def setup_admin_form(self):
        from .forms import AdminLoginForm
        admin.site.login_form = AdminLoginForm
