from django.shortcuts import render
from django.http import HttpResponse
from . models import Mebel


def show_all(request):
    mebels = Mebel.objects.all().order_by("-price")
    return render(
        request,
        'app_1/show_all.html',
        {'mebels': mebels}
    )
