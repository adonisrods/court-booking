import re
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,phone_number, password = None, **extra_fields):
        

        user=self.model(phone_number=phone_number, **extra_fields)
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, password , **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        return self.create_user( password, **extra_fields)
