from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Form, Division, Position, Notification, Skill, TimeKeeping


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

admin.site.register(Skill)
admin.site.register(Position)

class FormA(admin.ModelAdmin):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Form

admin.site.register(Form, FormA)

class NotificationA(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Notification

class DivisionA(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Division

