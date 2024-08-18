from django.shortcuts import render, HttpResponse

def store(request):
    return render(request, 'store/store.html')
