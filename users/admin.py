from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth import get_user_model
from .forms import UserAdminChangeForm,UserAdminCreationForm
from .models import Profile, Donator

"""
def get_readonly_fields(self, request, obj=None):
    if request.user.is_staff:
        if request.user.is_superuser:
            return []
        else:
            return [f.name for f in self.model._meta.fields]
"""



User=get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin','staff', 'autentifikacija')
    list_filter = ('admin','staff', 'autentifikacija')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'autentifikacija')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


    def get_readonly_fields(self, request, obj=None):
        if request.user.is_admin:
            return self.readonly_fields

        if self.get_fieldsets(request,obj) :
            return flatten_fieldsets(self.get_fieldsets(request,obj) )
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))



admin.site.unregister(Group)


admin.site.register(User, UserAdmin)
admin.site.register(Donator)
admin.site.register(Profile)
