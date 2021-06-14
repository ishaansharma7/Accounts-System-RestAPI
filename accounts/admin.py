from django.contrib import admin
from django.contrib import admin
from accounts.models import NewUser, TestTransaction
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'user_name')
    list_filter = ('is_active', 'is_staff', 'role')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'is_active', 'is_staff', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'age', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'role', 'groups')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'role')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
admin.site.register(TestTransaction)