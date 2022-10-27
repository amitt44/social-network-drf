from django.urls import path
from siimapp import views

urlpatterns = [
    path('api/register', views.Registration.as_view(), name='register'),
    path('api/login', views.LogIn.as_view(), name='login'),
    path('api/post', views.PostView.as_view(), name='posts'),
    path('api/post/<int:pk>', views.PostViewDetail.as_view(), name='post-by-id'),
    path('api/fav-post/<int:post_id>', views.FavouritePostView.as_view(), name='fav-post-by-id'),
]