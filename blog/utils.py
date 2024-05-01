import json
from .models import BlogPost, Comment, Category
from django.db.models import Q

# GET POST BASED ON CATEGORY FUNCTION
def get_blog_category_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.all().filter(
            Q(category__category_name__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))

# SEARCH POST FUNCTION
def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BlogPost.objects.all().filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))

# SEARCH CATEGORY FUNCTION
def get_category_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        category = Category.objects.all().filter(
            Q(category_name__icontains=q)
        ).distinct()
        for cat in category:
            queryset.append(cat)
    return list(set(queryset))


def commentFormData(request):
    pass
    user = request.user

    obj = json.loads(request.POST['comment_data'])
    post = BlogPost.objects.get(id=obj['post'])

    if user.is_authenticated:
        comment = Comment.objects.create(
            post=post,
            name_comment=user.name,
            email_comment=user.email,
            username_comment=user.username,
            content=obj['content']

            )
    else:
        comment = Comment.objects.create(
            post=post,
            name_comment=obj['name_comment'],
            email_comment=obj['email_comment'],
            username_comment=obj['username_comment'],
            content=obj['content'],
            

            )

    if obj['parent']:
        c = Comment.objects.all().filter(id=int(obj['parent']))
        comment.parent =c.first()
        comment.save()

    print(comment)