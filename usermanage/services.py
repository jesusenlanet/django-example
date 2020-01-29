from rest_framework.fields import empty
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from usermanage.forms import IbanUserForm
from usermanage.models import IbanUser
from usermanage.serializers import IbanUserSerializer


def create_user(request):
    """Create the sended user and return the serializer"""
    serializer = IbanUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['creator'] = request.user
        serializer.save()
    return serializer


def serialize_user(user, data=empty):
    """Given a model IbanUser instance, return the instance serialized"""
    serializer = IbanUserSerializer(user, data=data)
    return serializer


def get_user(request, pk):
    """Return the user identified by pk
    Check the if request.user owns that iban user
    :return: Tuple with the model instance and a status code:
            If user is not found, (None, HTTP_404_NOT_FOUND)
            If user is not owned by request.user: (None, HTTP_401_UNAUTHORIZED)
            If everything is ok: (iban_user_instance, HTTP_200_OK)
    """
    if IbanUser.objects.filter(pk=pk).exists():
        queryset = IbanUser.objects.filter(pk=pk)
    else:
        return None, HTTP_404_NOT_FOUND

    queryset = queryset.owner(request.user)
    if not queryset.exists():
        return None, HTTP_401_UNAUTHORIZED
    return queryset.first(), HTTP_200_OK


def get_creation_form(serializer):
    """Given a iban user serializer, return the appropriate form"""
    if serializer.is_valid():
        form = IbanUserForm()
    else:
        form = IbanUserForm(serializer.data)
    return form


def get_users_by_owner(request):
    """Return the a iban user queryset owned by request.user"""
    return IbanUser.objects.owner(request.user)
