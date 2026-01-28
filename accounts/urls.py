from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='loginpage'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='registerpage'),
    path('contact/', views.contact_view, name='contactpage'),
]
