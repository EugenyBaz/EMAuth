from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_staff", "is_superuser", "is_active")


admin.site.unregister(Group)


# Создаём свой админ
@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    list_display = ("id", "name", "members")
    search_fields = ("name",)

    def members(self, obj):
        return ", ".join([u.email for u in obj.user_set.all()])

    members.short_description = "Пользователи"
