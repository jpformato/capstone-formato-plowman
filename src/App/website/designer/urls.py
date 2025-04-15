from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('windowMain/', views.windowMain, name='windowMain'),
    # path('createCustomer/', views.create_customer, name='create_customer'),
    path('', views.login_view, name='login'),
    path('menu/', views.menu, name='menu'),
    path('progressbar/<int:project_id>/', views.progressbar, name='progressbar'),
    path('progress/update/', views.update_project_status, name='update_project_status'),
    path('logout/', views.logout_view, name='logout'),
    path('get-frames/', views.get_frames, name='get_frames'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('save-windows/', views.save_windows, name='save_windows')
]
