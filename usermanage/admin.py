from django.contrib import admin
from usermanage.models import IbanUser


class IbanUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'iban', 'first_name', 'last_name', 'creator')


# Register your models here.
admin.site.register(IbanUser, IbanUserAdmin)
