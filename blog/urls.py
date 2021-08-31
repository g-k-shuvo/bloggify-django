from django.urls import path
from .views import home, blog, topic, detail, like, search, author, create, edit, delete


urlpatterns = [
    path('', home, name='home'),
    path('blog/', blog, name='blog'),
    path('blog/<str:name>/', topic, name='topic'),
    path('detail/<int:pk>/', detail, name='detail'),
    path('like/<int:pk>/', like, name='like'),
    path('search/', search, name='search'),
    path('author/<str:username>/', author, name='author'),
    path('create/', create, name='create'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete')

]
