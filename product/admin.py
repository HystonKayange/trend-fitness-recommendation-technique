import mptt
from django.contrib import admin
from . import models
from .models import Product, Tag
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'date_published', 'date_updated']
    list_filter = ['tag']
    search_fields = ('name', 'description')


class TagAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "tag_name"
    list_display = (
        'tree_actions', 'indented_title', 'related_products_count',
        'related_products_cumulative_count'
    )
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = Tag.objects.add_related_count(
            qs,
            Product,
            'tag',
            'products_cumulative_count',
            cumulative = True
        )
        
        qs = Tag.objects.add_related_count(
            qs,
            Product,
            'tag',
            'products_count',
            cumulative = False
        )
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related Posts(for this specific tag)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related posts (in tree)'


admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TagAdmin)
