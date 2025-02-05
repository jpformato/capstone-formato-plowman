from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def linkex(request):
    return render(request, 'linkex.html', {})