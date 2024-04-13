from django.shortcuts import render

# Create your views here.
def index_view(request):

    context = {
        'page':'home',
    }
    return render(request, "fitness/index.html", context)