from django.urls import path

from members.apis import views

app_name = 'users'

urlpatterns = [
    path('', views.UserCreateGenericAPIView.as_view(), name='user_create'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
]
