from django.urls import path
from . import views

urlpatterns = [
    path('', views.audit_list_view, name='audit_list'),
    path('new/', views.create_audit_view, name='create_audit'),
    path('<int:audit_id>/', views.audit_detail_view, name='audit_detail'),
    path('<int:audit_id>/verify/', views.verify_audit_view, name='verify_audit'),
]