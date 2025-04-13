from django.contrib import admin
from .models import Idiom

@admin.register(Idiom)
class IdiomAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'level')
    search_fields = ('phrase', 'definition', 'translation')
