from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from hitcount.views import HitCountDetailView
from django.http import JsonResponse

from .models import BlogPost, Category, Comment
from .forms import CreateBlogPostForm, EditBlogPostForm
from .utils import commentFormData
from django.views.generic import ListView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from operator import attrgetter


# all categories
def category_list(request):
    category = Category.objects.all()
    context = {'category': category}

    return context


def create_blog_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('user:must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)

    try:
        if form.is_valid():
            a = form.cleaned_data['category']
            obj = form.save(commit=False)

            author = request.user
            obj.author = author
            obj.save()
            for i in a:
                obj.category.add(i)
            obj.save()
            messages.success(request, f'"{obj.title}" created!')
            form = CreateBlogPostForm()
    except:
        messages.success(request, f'"{obj.title}" already exist! you can rename {obj.title} to {obj.title}_part 2')
    context = {
        'form': form,
    }

    return render(request, "blog/create_blog.html", context)


# edit blog post
def edit_blog_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('user:must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    if request.POST:
        form = EditBlogPostForm(request.POST, request.FILES, instance=blog_post)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            messages.success(request, "Updated Successfully!")

    form = EditBlogPostForm(
        initial={
            "title": blog_post.title,
            "category": blog_post.category.all(),
            "body": blog_post.body,
            "image": blog_post.image_url,
        }
    )

    context['form'] = form
    return render(request, 'blog/', context)


POSTS_PER_PAGE = 9


# blog pages
def blog_view(request):
    context = {}

    all_post = sorted(BlogPost.objects.all(), key=attrgetter('date_updated'), reverse=True)
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

    return render(request, 'blog/blog.html', context)


class DetailPostView(HitCountDetailView):
    model = BlogPost
    template_name = 'blog/detail_blog.html'
    context_object_name = 'post'
    slug_field = 'slug'
    count_hit = True

    def get_queryset(self):
        posts = BlogPost.objects.all().filter(slug=self.kwargs['slug'])
        return posts

    def get_context_data(self, **kwargs):
        context = super(DetailPostView, self).get_context_data(**kwargs)
        user = self.request.user
        post = self.get_queryset()
        post = post.first()

        cat = post.category
        related_post = BlogPost.objects.filter(category=cat).exclude(slug=self.kwargs['slug'])
        related_post = related_post.annotate(tag_count=Count('category')).order_by('-tag_count', '-date_published')

        comments = post.comments.all()

        context.update({
            'popular_posts': BlogPost.objects.order_by('-hit_count_generic__hits')[:3],
            'related_post':related_post[:1],
            'comments': comments,
            'user': user,
            'cat': cat,
        })
        return context


def comment_view(request):
    if request.POST:
        commentFormData(request)
    return JsonResponse("comment success", safe=False)


def commet_reply_view(request):
    print(request.POST)
    return JsonResponse('yes', safe=False)


def delete_post(request):
    posts = request.POST['deleteData']
    post = BlogPost.objects.get(id=posts)
    post.delete()

    return JsonResponse('post deleted', safe=False)


# category view
class CatListView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {}

        post = sorted(BlogPost.objects.all().filter(
            category__category_name=self.kwargs['category']), key=attrgetter('date_updated'), reverse=True)

        content = {
            'cat': self.kwargs['category'],
            'posts': post,
        }

        return content
