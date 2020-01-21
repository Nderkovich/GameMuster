from django.shortcuts import render


def mainpage(request):
    return render(request, 'Games/list.html')


def detailpage(request):
    return render(request, 'Games/info.html')
