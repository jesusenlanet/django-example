from rest_framework import serializers

from usermanage.models import IbanUser


class IbanUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IbanUser
        fields = ['id', 'iban', 'first_name', 'last_name']
