# import the logging library
import logging
from django.contrib.auth.models import Permission

logger = logging.getLogger(__name__)


def make_staff(backend, user, *args, **kwargs):
    is_mew = kwargs.get('is_new', False)

    if backend.name == 'google-oauth2' and is_mew:
        user.is_staff = True
        if not user.has_perm('auth.view_user'):
            permission = Permission.objects.get(codename='view_user')
            user.user_permissions.add(permission)
        user.save()
