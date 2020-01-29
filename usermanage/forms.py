from django.forms import ModelForm

from usermanage.models import IbanUser


class IbanUserForm(ModelForm):
    class Meta:
        model = IbanUser
        fields = ('iban', 'first_name', 'last_name')
