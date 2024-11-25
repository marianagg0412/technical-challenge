from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('login/', views.CustomLoginView.as_view(), name='login'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('control/header/<int:control_id>/', views.control_header, name='control_header'),
   path('control/design/<int:control_id>/', views.control_design, name='control_design'),
]