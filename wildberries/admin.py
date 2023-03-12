from django.contrib import admin

from wildberries.models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        'article',
        'brand',
        'title',
    ]
    search_fields = (
        'article',
    )
