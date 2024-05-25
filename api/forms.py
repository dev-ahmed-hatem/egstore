from django.contrib.auth.admin import UserAdmin as UA
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm as UserCreation, UserChangeForm as UserChange
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import UserProfile


class UserChangeForm(UserChange):
    class Meta:
        model = UserProfile
        fields = (
            'phone_number', 'username', 'first_name', 'last_name', 'password', 'is_active', 'is_admin',
            'is_superuser', 'user_permissions')
        widgets = {
            'user_permissions': FilteredSelectMultiple("Permissions", is_stacked=False),
        }


class UserCreationForm(UserCreation):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'username', 'first_name', 'last_name', 'password')


class UserAdmin(UA):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["phone_number", "username", "full_name", "is_admin"]
    list_filter = ["is_admin", "username", "phone_number"]
    fieldsets = [
        ("Personal Information", {
            "fields": ["first_name", "last_name", "picture"]
        }),
        ("Authentication", {
            "fields": ["phone_number", "username", "password"]
        }),
        ("Permissions", {
            "fields": ["is_active", "is_admin", "is_superuser", "user_permissions"]
        })
    ]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active',
                'is_admin',
                'is_superuser'),
        }),
    )

    filter_horizontal = []

    @admin.display(description="Name")
    def full_name(self, user):
        return f"{user.first_name} {user.last_name}"
