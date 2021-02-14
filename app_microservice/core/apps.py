from django.apps import AppConfig
from django.contrib import admin
from django.db.models.signals import pre_delete


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        self.setup_admin_form()
        self.setup_signals()

    def setup_admin_form(self):
        from .forms import AdminLoginForm
        admin.site.login_form = AdminLoginForm

    def setup_signals(self):
        from .models import Offer
        from .signals import delete_offer_images

        pre_delete.connect(
            delete_offer_images,
            sender=Offer,
            dispatch_uid='core.signals.delete_offer_images'
        )
