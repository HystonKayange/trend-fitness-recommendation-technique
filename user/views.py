from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def profile_form_view(request, username):

    context = {}
    if request.POST == "POST":
        return JsonResponse(request, context, safe=False)
    return render(request, "account/profile_form.html")
