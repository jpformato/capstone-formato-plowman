from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .class_functions.project import create_project, read_project, update_project
from .class_functions.project_detail import create_project_detail, read_project_detail
from .class_functions.preview import create_preview, read_preview
from .class_functions.window import create_window, read_window
from .class_functions.window import read_frame
from .models import Project, ProjectStatus, Status, Frame, Project_Detail, Preview, Window
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden, JsonResponse, Http404, HttpResponse
from django.contrib.messages import get_messages
import json
from django.utils.dateparse import parse_date
from datetime import datetime
import base64
from django.contrib.messages import get_messages

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
    opening_project = request.session.get('opening_project', False)
    return render(request, 'windowMain.html', {
        'opening_project': opening_project
    })

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pswd')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            storage = get_messages(request)
            for _ in storage:
                pass  # clears the queue

            return redirect('menu')
        else:
            # GO BACK AND MAKE THE MESSAGE
            messages.error(request, "Invalid credentials")
            return redirect('/')
        
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    return redirect('/')

def menu(request):
    if request.method == 'POST':
        customer_email = request.POST.get('customer_email')
        employee_id = request.user.id

        project = create_project(customer_email=customer_email, employee_id=employee_id)
        if project is None:
            messages.error(request, "Failed to create project")
            return redirect('menu')
        else:
            request.session['project_id'] = project.project_id
            request.session['detail_id'] = None
            request.session['preview_id'] = None
            request.session['opening_project'] = False
            return redirect('windowMain')
    return render(request, 'menu.html', {})

@login_required
def my_jobs(request):
    user = request.user
    projects = Project.objects.filter(employees=user)

    context = {
        'projects': projects
    }
    return render(request, 'my_jobs.html', context)

@staff_member_required
def job_list(request):
    projects = Project.objects.all()

    context = {
        'projects': projects
    }
    return render(request, 'job_list.html', context)

@login_required
def progressbar(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    all_steps = Status.objects.all().order_by('status_id')
    progress = ProjectStatus.objects.filter(project=project)

    is_editable = request.user.is_authenticated and request.user.is_staff

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
        'is_editable': request.user.is_staff,  # Only staff can edit
    }
    return render(request, 'progressbar.html', context)

def get_frames(request):
    frames = Frame.objects.all()
    frame_data = []
    for frame in frames:
        if frame.image:
            image_data = base64.b64encode(frame.image).decode('utf-8')
            frame_data.append({
                'id': frame.frame_id,
                'name': frame.name,
                'image': f'data:image/png;base64,{image_data}',
            })
    return JsonResponse({'frames': frame_data})

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_bytes = image.read()
        project_id = request.session['project_id']

        project = read_project(project_id)
        if project is None:
            return JsonResponse({'success': False, 'error': 'Project not found'}, status=404)

        # Check if image exists
        existing_detail = Project_Detail.objects.filter(
            project=project,
            image=image_bytes
        ).first()

        if existing_detail:
            request.session['detail_id'] = existing_detail.project_detail_id
            return JsonResponse({'success': True, 'message': 'Image already exists'})

        detail = Project_Detail.objects.create(
            project=project,
            image=image_bytes
        )

        request.session['detail_id'] = detail.project_detail_id
        return JsonResponse({'success': True, 'message': 'Image uploaded successfully'})

    return JsonResponse({'success': False, 'error': 'No image uploaded'}, status=400)

def save_windows(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            windows = data.get('windows', [])
            preview = create_preview(request.session['detail_id'])
            if preview is None:
                return JsonResponse({'success': False,'error': 'Could not create or retrieve preview.'}, status=400)
            request.session['preview_id'] = preview.preview_id

            # Loop through the windows data and save each one
            print(windows)
            for window in windows:
                create_window(
                    preview_id=preview.preview_id,  # Assign the correct preview
                    x1=window['x1'],
                    y1=window['y1'],
                    x2=window['x2'],
                    y2=window['y2'],
                    frame_id=window['frameId'],
                )
            print("YES")
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def get_previews(request, project_id):
    previews = []
    project = read_project(project_id=project_id)
    
    if project is None:
        print("NONE")
        return

    for detail in project.details.all():
        for preview in detail.previews.all():
            previews.append({
                'preview_id': preview.preview_id,
                'save_date': preview.save_date.strftime('%Y-%m-%d'),
                'final': preview.final,
            })
    return JsonResponse(previews, safe=False)

@login_required
def load_project(request, preview_id):
    preview = read_preview(preview_id=preview_id)
    if preview is None:
        raise Http404("Preview not found")


    # Save IDs to session for later reference
    request.session['preview_id'] = preview.preview_id
    request.session['detail_id'] = preview.detail.project_detail_id
    request.session['project_id'] = preview.detail.project.project_id
    request.session['opening_project'] = True

    return redirect('windowMain')  # This should launch the designer view

def get_detail_image(request):
    if request.session['detail_id'] is None:
        raise Http404("Detail is none")
    
    detail = read_project_detail(request.session['detail_id'])
    if detail is None:
        raise Http404("Detail not found")
    
    # if detail.image[:3] == b'\xFF\xD8\xFF':
    #     content_type = 'image/jpeg'
    # else:
    #     content_type = 'image/png'

    return HttpResponse(detail.image, content_type='image/*')

def get_windows(request):
    windows = []
    preview = read_preview(preview_id=request.session['preview_id'])
    if preview is None:
        raise Http404("Preview not found")
    
    for window in preview.windows.all():
        if window.frame is not None:
            windows.append({
                'x1': window.x1,
                'x2': window.x2,
                'y1': window.y1,
                'y2': window.y2,
                'frame_id': window.frame.frame_id
            })
        else:
            windows.append({
                'x1': window.x1,
                'x2': window.x2,
                'y1': window.y1,
                'y2': window.y2,
                'frame_id': None
            })

    return JsonResponse(windows, safe=False)

def get_window_frame(request, frame_id):
    print(frame_id)
    frame = read_frame(frame_id)
    if frame is None:
        raise Http404("Detail not found")
    
    return HttpResponse(frame.image, content_type='image/*')