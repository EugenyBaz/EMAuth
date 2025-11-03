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

    def members(self, group_instance):
        return ", ".join([user.email for user in group_instance.user_set.all()])

    members.short_description = "Пользователи"
