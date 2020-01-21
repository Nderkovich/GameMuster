from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def mainpage(request: HttpRequest) -> HttpResponse:
    return render(request, 'Games/list.html')


def detailpage(request: HttpRequest) -> HttpResponse:
    return render(request, 'Games/info.html')
