from django.urls import path

from members.apis import views

app_name = 'users'

urlpatterns = [
    path('/', views.UserCreateGenericAPIView.as_view(), name='user_create'),
]
