from django.shortcuts import render, redirect
from .forms import FitnessGoalsForm
from blog.models import BlogPost
from product.models import Product
from operator import attrgetter
#from blog.utils import get_blog_queryset, get_category_queryset, get_blog_category_queryset
"""from operator import attrgetter
from blog.models import BlogPost, Category, Comment

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator"""

def index_view(request):
    all_post = sorted(BlogPost.objects.all(), key=attrgetter('date_updated'), reverse=True)
    product = sorted(Product.objects.all(), key=attrgetter('date_updated'), reverse=True)
    context = {
        'page': 'home',
        'all_post': all_post[:6],
        'all_product': product[:6]
    }
    return render(request, "fitness/index.html", context)


def personization_data(request):
    if request.method == 'POST':
        form = FitnessGoalsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fitness:personization')
    else:
        form = FitnessGoalsForm()
    return render(request, 'fitness/personization.html', {'form': form})

"""
def search_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET.get('q')
        context['query'] = str(query)

        posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)

        # Pagination
        POSTS_PER_PAGE = 6
        page = request.GET.get('page', 1)
        post_paginator = Paginator(posts, POSTS_PER_PAGE)

        try:
            posts = post_paginator.page(page)
        except PageNotAnInteger:
            posts = post_paginator.page(POSTS_PER_PAGE)
        except EmptyPage:
            posts = post_paginator.page(post_paginator.num_pages)

        category = get_category_queryset(query)

        context = {
            'all_post': posts,
            'category':category,
            'query': query,
        }
    return render(request, 'fitness/search.html', context)
"""