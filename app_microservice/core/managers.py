from django.contrib.auth.models import BaseUserManager


class WSUserManager(BaseUserManager):
    """ Database manager for user accounts. """
    def create_user(self, email, password=None, **extra_fields):
        """ Create and save a user with the given email address. """
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, password=None, **extra_fields):
        """ Create and save an admin user with the given email address. """
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(password=password, **extra_fields)

    def _create_user(self, email=None, password=None, **extra_fields):
        user = self.model(**extra_fields)

        if email is not None:
            user.email = email

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user
