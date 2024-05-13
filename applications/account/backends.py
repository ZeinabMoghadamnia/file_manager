from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(phone_number__iexact=username) | Q(email__iexact=username))
            if user.check_password(password):
                return user
            messages.error(request, _(f"The username(Email) or password is incorrect !"), 'danger')
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None