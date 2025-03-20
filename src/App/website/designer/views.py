from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .class_functions.project import create_project, read_project, update_project

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def windowMain(request):
    return render(request, 'windowMain.html', {})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/')
        
    return render(request, 'login.html', {})

def menu(request):
    return render(request, 'menu.html', {})


# def create_customer(request):
#     if request.method == 'POST':
#         email = request.POST["email"]
#         first_name = request.POST["first_name"]
#         last_name = request.POST["last_name"]
#         username = request.POST["username"]
#         password = request.POST["password"]

#         person = read_person(email)

#         if not person:
#             messages.error(request, "No person found with this email")
#             return render(request, 'createCustomer.html', {})
        
#         if not check_new_password(email):
#             messages.error(request, "Account already created")
#             return render(request, "createCustomer.html")
        
#         attributes = {
#             'email'      : person.email,
#             'first_name' : first_name,
#             'last_name'  : last_name,
#             'username'   : username,
#             'password'   : password,
#             'department' : person.department,
#         }

#         saved = update_person(attributes)
#         if not saved:
#             messages.error(request, "Failed to create")
#             return render(request, "createCustomer.html")

#         return redirect("index")

#     return render(request, 'createCustomer.html', {})

