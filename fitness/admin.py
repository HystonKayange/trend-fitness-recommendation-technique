from django.contrib import admin
from .models import (
        FrequentlyAskedQuestion,
        TopSearch,
    )


class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date']
    search_fields = ['title', 'content']


class TopSearchAdmin(admin.ModelAdmin):
    list_display = ['name', 'search_count']
    search_fields = ['name']


admin.site.register(FrequentlyAskedQuestion, FAQAdmin)
admin.site.register(TopSearch, TopSearchAdmin)