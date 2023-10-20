from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User
from core.forms import UserChangeForm,UserCreationForm


# Register your models here.
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("phone_number", "is_staff", "is_active",)
    list_filter = ("phone_number", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("phone_number",)
    ordering = ("phone_number",)

admin.site.register(User, UserAdmin)