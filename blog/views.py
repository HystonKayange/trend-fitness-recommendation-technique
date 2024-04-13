from django.shortcuts import render


def blog_view(request):
    return render(request, "blog/blog.html")
