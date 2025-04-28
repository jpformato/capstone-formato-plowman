from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('windowMain/', views.windowMain, name='windowMain'),
    # path('createCustomer/', views.create_customer, name='create_customer'),
    path('', views.login_view, name='login'),
    path('menu/', views.menu, name='menu'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('job-list/', views.job_list, name='job_list'),
    path('load-project/<int:preview_id>/', views.load_project, name='load_project'),
    path('progressbar/<str:order_number>/', views.progressbar, name='progressbar'),
    path('progress/update/', views.update_project_status, name='update_project_status'),
    path('logout/', views.logout_view, name='logout'),
    path('get-frames/', views.get_frames, name='get_frames'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('save-windows/', views.save_windows, name='save_windows'),
    path('get-previews/<int:project_id>/', views.get_previews, name='get_previews'),
    path('get-detail-image/', views.get_detail_image, name="get_detail_image"),
    path('get-windows/', views.get_windows, name='get_windows'),
    path('get-window-frame/<int:frame_id>/', views.get_window_frame, name='get_window_frame'),
    path('get-project-id/<str:order_number>/', views.get_project_id, name='get_project_id')
]
