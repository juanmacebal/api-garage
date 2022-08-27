from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    ordering = ('-is_superuser', '-is_staff', 'last_name', 'first_name')
    list_filter = (
        'is_superuser',
        'is_staff',
        'is_active'
    )
    search_fields = (
        'first_name',
        'last_name',
        'email'
    )
    list_display = (
        'last_name',
        'first_name',
        'email',
        'is_superuser',
        'is_staff',
        'is_active'
    )
    readonly_fields = ['last_login']
    fieldsets = (
        (_('Login'), {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('last_name', 'first_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (_('Login'), {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
        (_('Personal Info'), {'fields': ('last_name', 'first_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )


admin.site.register(get_user_model(), UserAdmin)
admin.site.unregister(Group)
admin.site.site_header = _('Garage Administration')
