from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.posts_index, name='posts_index'),
    path('profile/', views.profile_index, name='profile_index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('posts/<int:post_id>/', views.posts_detail, name='detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])