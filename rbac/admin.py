from django.contrib import admin
from rbac import models
from werkzeug.security import generate_password_hash

class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'menu']


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', 'feature', 'group_menu', 'group']


class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password_hash', ]
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """

        obj.password_hash =  str(generate_password_hash(obj.password_hash))
        print(obj.password_hash)
        print(obj.__dict__)

        obj.save()


admin.site.register(models.Menu)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.Role, RoleAdmin)
