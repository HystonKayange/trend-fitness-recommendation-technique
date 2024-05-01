from django.shortcuts import render
from django.db.models import Count
from hitcount.views import HitCountDetailView
from django.views.generic import ListView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from operator import attrgetter
from .models import Tag, Product


POSTS_PER_PAGE = 9


# product pages
def product_view(request):
    context = {}

    all_post = sorted(Product.objects.all(), key=attrgetter('date_updated'), reverse=True)
    context['all_post'] = all_post

    # Pagination
    page = request.GET.get('page', 1)
    all_post_paginator = Paginator(all_post, POSTS_PER_PAGE)

    try:
        all_post = all_post_paginator.page(page)
    except PageNotAnInteger:
        all_post = all_post_paginator.page(POSTS_PER_PAGE)
    except EmptyPage:
        all_post = all_post_paginator.page(all_post_paginator.num_pages)
    context['all_post'] = all_post

    return render(request, 'product/product.html', context)


class DetailProductView(HitCountDetailView):
    model = Product
    template_name = 'product/detail_product.html'
    context_object_name = 'product'
    slug_field = 'slug'
    count_hit = True

    def get_queryset(self):
        posts = Product.objects.all().filter(slug=self.kwargs['slug'])
        return posts

    def get_context_data(self, **kwargs):
        context = super(DetailProductView, self).get_context_data(**kwargs)
        product = self.get_queryset()
        product = product.first()

        tag = product.tag
        related_product = Product.objects.filter(tag=tag).exclude(slug=self.kwargs['slug'])
        related_product = related_product.annotate(tag_count=Count('tag')).order_by('-tag_count', '-date_published')

        context.update({
            'popular_product': Product.objects.order_by('-hit_count_generic__hits')[:3],
            'related_product':related_product[:1],
            'tag': tag,
        })
        return context


# tag view
class TagListView(ListView):
    template_name = 'product/tag.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {}

        product = sorted(Product.objects.all().filter(
            tag__tag_name=self.kwargs['tag']), key=attrgetter('date_updated'), reverse=True)

        content = {
            'tag': self.kwargs['tag'],
            'posts': product,
        }

        return content
