from django.urls import path
from .views import profile, update, register, login, logout

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('update/', update, name='update'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout')
]
