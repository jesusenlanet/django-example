from http.client import HTTPResponse

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.exceptions import MethodNotAllowed

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from usermanage.models import IbanUser
from usermanage.serializers import IbanUserSerializer


def index(request):
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


class IbanUserView(APIView):
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(self.allowed_methods, 'Method now allowed')


class IbanUserList(IbanUserView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = 'list.html'

    def get(self, request):
        queryset = IbanUser.objects.all()
        return Response({'iban_users': queryset})


class IbanUserDetail(IbanUserView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = 'detail.html'

    def get(self, request, pk):
        iban_user = get_object_or_404(IbanUser, pk=pk)
        serializer = IbanUserSerializer(iban_user)
        return Response({'serializer': serializer, 'iban_user': iban_user})

    def post(self, request, pk):
        iban_user = get_object_or_404(IbanUser, pk=pk)
        serializer = IbanUserSerializer(iban_user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'iban_user': iban_user})
        serializer.save()
        return redirect('user-list')


class IbanUserDelete(IbanUserView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # user = request.user
        iban_user = get_object_or_404(IbanUser, pk=pk)
        iban_user.delete()
        return redirect('user-list')
