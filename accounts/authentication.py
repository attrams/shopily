from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameAuthBackend(ModelBackend):

    '''
    Authenticate using e-mail address or username.
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            '''
            The line below can simply be written as `user = User.objects.get(email=username)`
            or `user = User.objects.get(email__iexact=username)` for case insensitive.

            The reason why you could replace the line is because, the `ModelBackend` authentication
            already performs the query using the username (...get(username=username))). The `ModelBackend`
            is the default authentication used.

            Since a custom authentication is going to be used, the `settings.py` file will include
            AUTHENTICATION_BACKENDS = [
                'accounts.authentication.EmailOrUsernameAuthBackend', # the order matters
                'django.contrib.auth.backends.ModelBackend', # because this already uses the username if the custom authentication fails django will use this.
            ]
            '''
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )

            if user.check_password(password):
                return user

            return None

        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None
