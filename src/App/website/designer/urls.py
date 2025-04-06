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

]
