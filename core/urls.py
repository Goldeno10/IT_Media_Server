from django.urls import path
from .views import login_view, logout_view, registration_view


app_name = 'core'

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', registration_view, name='register'),
]

