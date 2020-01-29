from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render, redirect

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.views import APIView

from usermanage.forms import IbanUserForm
from usermanage.services import get_users_by_owner, get_creation_form, get_user, serialize_user, create_user


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


class IbanUserView(APIView):
    """Base class for the API view"""
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self.allowed_methods, 'Method now allowed')


class IbanUserList(IbanUserView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = 'list.html'

    def get(self, request):
        """Retrieve a list of users"""
        queryset = get_users_by_owner(request)
        form = IbanUserForm()
        return Response({'iban_users': queryset, 'form': form})

    def post(self, request):
        """Create a user"""
        queryset = get_users_by_owner(request)
        serializer = create_user(request)
        if serializer.is_valid():
            status_code = HTTP_201_CREATED
        else:
            status_code = HTTP_422_UNPROCESSABLE_ENTITY
        form = get_creation_form(serializer)
        return Response({'iban_users': queryset, 'form': form}, status=status_code)


class IbanUserDelete(IbanUserView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Delete a iban user"""
        iban_user, status = get_user(request, pk)
        if status != HTTP_200_OK:
            return HttpResponse(status=status)
        iban_user.delete()
        return render(request, 'deleted.html')


class IbanUserDetail(IbanUserView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = 'detail.html'

    def get(self, request, pk):
        """Retrieve a single iban user"""
        iban_user, status = get_user(request, pk)
        if status != HTTP_200_OK:
            return HttpResponse(status=status)

        serializer = serialize_user(iban_user)
        return Response({'serializer': serializer, 'iban_user': iban_user})

    def post(self, request, pk):
        """Update a iban user"""
        iban_user, status = get_user(request, pk)
        if status != HTTP_200_OK:
            return HttpResponse(status=status)

        serializer = serialize_user(iban_user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'iban_user': iban_user}, status=HTTP_422_UNPROCESSABLE_ENTITY)

        serializer.save()
        return render(request, 'updated.html')
