from django.urls import path

from repository.apis import views

app_name = 'repository'

urlpatterns = [
    path('', views.RepositoryListCreateGenericAPIView.as_view(), name='repository_list_create'),
    path('<int:pk>/',
         views.RepositoryRetrieveUpdateDestroyGenericAPIView.as_view(),
         name='repository_retrieve_update_destroy')
]
