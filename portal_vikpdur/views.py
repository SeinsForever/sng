from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def index(request):
    host = request.META["HTTP_HOST"]
    try:
        name = request.COOKIES["name"]
    except:
        name = "undef"
    return HttpResponse(f"name:{name}")

def api_user_auth(request):
    name = request.GET.get("name", "Undefined")
    response = HttpResponse(f"name:{name}")
    response.set_cookie("name", name)
    return HttpResponse(response)
    # return HttpResponseRedirect("")
