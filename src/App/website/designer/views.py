from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def windowMain(request):
    return render(request, 'windowMain.html', {})