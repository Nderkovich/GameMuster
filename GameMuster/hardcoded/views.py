from django.shortcuts import render

# Create your views here.
def mainpage(request):
    return render(request, 'hardcoded/list.html')

def detailpage(request):
    return render(request, 'hardcoded/info.html')