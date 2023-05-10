from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from main_app.views import SignUp

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('posts/', views.PostList.as_view(), name='posts_index'),
    path('posts/create/', views.PostCreate.as_view(), name='posts_create'),
    path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='posts_update'),
    path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='posts_delete'),
    path('posts/like/<int:pk>', views.like_post, name='like_post'),
    path('posts/<int:pk>/add_comment', views.CommentCreate.as_view(), name='comment_create'),
    # path('posts/like/<int:pk>', views.unlike_post, name='unlike_post'),
    path('profile/', views.profile_index, name='profile_index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('posts/<int:post_id>/', views.posts_detail, name='posts_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])