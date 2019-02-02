from django.urls import path

from members.apis import views

app_name = 'users'

urlpatterns = [
    path('', views.UserCreateGenericAPIView.as_view(), name='user_create'),
    path('<int:pk>/', views.UserProfileGenericAPIView.as_view(), name='user_profile'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
]
