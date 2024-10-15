from django.contrib import admin
from .models import Feature, Contact
# Register your models here.

admin.site.register(Feature)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')