from django.contrib import admin
from .models import *
from .forms import AppListForm


# Register your models here.

class AplicationAdmin(admin.ModelAdmin):
    form = AppListForm
    list_filter = ('status',)
    list_display = ('status', 'name', 'date', 'Category',)
    fields = ('status', 'photo_file', 'photo_file2', 'description', 'Category', 'comment')


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Aplication, AplicationAdmin)
