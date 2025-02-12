from django.shortcuts import render, redirect
from django.contrib import messages
from .class_functions.person import read_person, check_new_password, update_person

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def windowMain(request):
    return render(request, 'windowMain.html', {})

def create_customer(request):
    if request.method == 'POST':
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]

        person = read_person(email)

        if not person:
            messages.error(request, "No person found with this email")
            return render(request, 'createCustomer.html', {})
        
        if not check_new_password(email):
            messages.error(request, "Account already created")
            return render(request, "createCustomer.html")
        
        person['first_name'] = first_name
        person['last_name'] = last_name
        person['username'] = username
        person['password'] = password

        saved = update_person(person)
        if not saved:
            messages.error(request, "Failed to create")
            return render(request, "createCustomer.html")

        return redirect("index")

    return render(request, 'createCustomer.html', {})

