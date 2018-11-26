from django.contrib import admin
from upload_file import models


class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'excel_name', 'sheet_num', 'flag', 'date', 'txt']


class TxtAdmin(admin.ModelAdmin):
    list_display = ['id', 'txt_name', 'txt_result', ]


admin.site.register(models.File, FileAdmin)
admin.site.register(models.Txt, TxtAdmin)
