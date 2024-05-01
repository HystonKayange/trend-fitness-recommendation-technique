import mptt
from django.contrib import admin
from . import models
from .models import BlogPost, Category
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_published', 'date_updated']
    list_filter = ['category']
    search_fields = ('title', 'body')


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "category_name"
    list_display = (
        'tree_actions', 'indented_title', 'related_products_count',
        'related_products_cumulative_count'
    )
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = Category.objects.add_related_count(
            qs,
            BlogPost,
            'category',
            'products_cumulative_count',
            cumulative = True
        )
        
        qs = Category.objects.add_related_count(
            qs,
            BlogPost,
            'category',
            'products_count',
            cumulative = False
        )
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related Posts(for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related posts (in tree)'


admin.site.register(BlogPost, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(models.Comment, MPTTModelAdmin)