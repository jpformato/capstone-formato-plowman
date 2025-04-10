from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .class_functions.project import create_project, read_project, update_project
from .models import Project, ProjectStatus, Status
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils.dateparse import parse_date
from datetime import datetime

@require_POST
@csrf_exempt
def update_project_status(request):
    try:
        data = json.loads(request.body)
        project_id = data.get("project_id")
        step_name = data.get("step_name")
        start_date = data.get("start_date")  # Format: MM/DD/YY
        end_date = data.get("end_date")      # Format: MM/DD/YY
        notes = data.get("notes")

        def parse_mmddyy(date_str):
            return datetime.strptime(date_str, "%m/%d/%y").date()

        project = Project.objects.get(pk=project_id)
        status = Status.objects.get(name=step_name)

        project_status, _ = ProjectStatus.objects.get_or_create(project=project, status=status)

        changed = False

        if start_date:
            project_status.start_date = parse_mmddyy(start_date)
            changed = True

        if end_date:
            project_status.end_date = datetime.combine(parse_mmddyy(end_date), datetime.min.time())
            changed = True

        if notes is not None:
            if hasattr(project_status, 'notes'):
                project_status.notes = notes
                changed = True

        if changed:
            project_status.save()

        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def windowMain(request):
    return render(request, 'windowMain.html', {})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pswd')
        print(email)

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/')
        
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('/')

def menu(request):
    return render(request, 'menu.html', {})

def progressbar(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    all_steps = Status.objects.all().order_by('status_id')
    progress = ProjectStatus.objects.filter(project=project)

    # Build a dictionary of progress by status name
    progress_dict = {
        ps.status.name: {
            'start_date': ps.start_date.strftime('%m/%d/%y') if ps.start_date else '',
            'end_date': ps.end_date.strftime('%m/%d/%y') if ps.end_date else '',
            'notes': ps.notes if hasattr(ps, 'notes') else ''
        }
        for ps in progress
    }

    context = {
        'project': project,
        'steps': all_steps,
        'progress': progress_dict,
    }
    return render(request, 'progressbar.html', context)
