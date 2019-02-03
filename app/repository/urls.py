from django.urls import path

from repository.apis import views

app_name = 'repository'

urlpatterns = [
    path('', views.RepositoryListCreateGenericAPIView.as_view(), name='repository_list_create'),
    path('<int:pk>/',
         views.RepositoryRetrieveUpdateDestroyGenericAPIView.as_view(),
         name='repository_retrieve_update_destroy'),
    path('file/',
         views.ManagedFileListCreateGenericAPIView.as_view(),
         name='managed_file_list_create')
]
