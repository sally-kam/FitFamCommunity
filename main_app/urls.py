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
    path('posts/<int:pk>/like', views.like_post2, name='like_post2'),
    path('posts/<int:pk>/add_comment/', views.CommentCreate.as_view(), name='comments_create'),
    path('posts/add_comment/<int:pk>/', views.CommentCreate2.as_view(), name='comments_create2'),
    # path('posts/<int:post_pk>/update_comment/<int:pk>/', views.CommentUpdate.as_view(), name='comments_update'),
    path('posts/<int:post_pk>/delete_comment/<int:pk>/', views.CommentDelete.as_view(), name='comments_delete'),
    # path('posts/like/<int:pk>', views.unlike_post, name='unlike_post'),
    path('profile/', views.profile_index, name='profile_index'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('posts/<int:post_id>/', views.posts_detail, name='posts_detail'),
    path('resources/foodcaloriecounter', views.food_calorie_counter, name='food_calorie_counter'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])