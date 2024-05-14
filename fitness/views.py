from django.shortcuts import render
from operator import attrgetter
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from operator import attrgetter
from product.models import Product, Tag
from blog.models import BlogPost, Category
from .models import TopSearch, FrequentlyAskedQuestion


def index_view(request):
    all_post = sorted(BlogPost.objects.all(), key=attrgetter('date_updated'), reverse=True)
    product = sorted(Product.objects.all(), key=attrgetter('date_updated'), reverse=True)
    context = {
        'page': 'home',
        'all_post': all_post[:6],
        'all_product': product[:6]
    }
    return render(request, "fitness/index.html", context)


# SEARCH POST FUNCTION
def get_product_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        product = Product.objects.all().filter(
            Q(name__icontains=q) |
            Q(price__icontains=q) |
            Q(tag__tag_name__icontains=q) |
            Q(description__icontains=q)
        ).distinct()
        for products in product:
            queryset.append(products)
    return list(set(queryset))

def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        post = BlogPost.objects.all().filter(
            Q(title__icontains=q) |
            Q(category__category_name__icontains=q) |
            Q(body__icontains=q) 
        ).distinct()
        for post in post:
            queryset.append(post)
    return list(set(queryset))


def get_faq_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        service = FrequentlyAskedQuestion.objects.all().filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        ).distinct()
        for services in service:
            queryset.append(services)
    return list(set(queryset))


def search_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q')
        context['query'] = str(query)
        
        top_search, created = TopSearch.objects.get_or_create(name=query)
        top_search.search_count += 1
        top_search.save()
        
        product = sorted(get_product_queryset(query), key=attrgetter('date_updated'), reverse=True)
        post = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)

        # Pagination
        POSTS_PER_PAGE = 9
        page = request.GET.get('page', 1)
        product_paginator = Paginator(product, POSTS_PER_PAGE)
        post_paginator = Paginator(product, POSTS_PER_PAGE)

        try:
            product = product_paginator.page(page)
            post = post_paginator.page(page)
        except PageNotAnInteger:
            product = product_paginator.page(POSTS_PER_PAGE)
            post = post_paginator.page(POSTS_PER_PAGE)
        except EmptyPage:
            product = product_paginator.page(product_paginator.num_pages)
            post = post_paginator.page(post_paginator.num_pages)

        faq = get_faq_queryset(query)
        
        #search result couter
        """if product:
            for items in product:
                search_result, _ = ProductSearch.objects.get_or_create(product=items)
                search_result.search_count += 1
                search_result.save()
        if post:
            for items in post:
                search_result, created = CleanServiceSearch.objects.get_or_create(post=items)
                search_result.search_count += 1
                search_result.save()"""

        context = {
            'all_product': product,
            'post': post,
            'faq_content': faq,
            'query': query,
            'top_search': TopSearch.objects.all()[:6]
        }
    return render(request, 'fitness/search.html', context)


def faq_views(request):
    context = {
        'faq': True,
        'faq_content': FrequentlyAskedQuestion.objects.all(),
    }
    return render(request, "fitness/faqs.html", context)