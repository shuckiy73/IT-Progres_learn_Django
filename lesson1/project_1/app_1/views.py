from django.shortcuts import render
from django.http import HttpResponse


def url1(request):
    return HttpResponse("Ответ 1")


def url2(request):
    return HttpResponse("Ответ 2")


def url3(request):
    return HttpResponse("Ответ 3")

def url4(request):
    return HttpResponse("Ответ 4")

def url5(request):
    return HttpResponse(request)
