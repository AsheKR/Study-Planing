from django.urls import path, include

from repository.apis import views

app_name = 'repository'

file_patterns = ([
    path('file/',
         views.ManagedFileCreateGenericAPIView.as_view(),
         name='managed_file_create'),
    path('<int:repository_pk>/directory/<int:dir_pk>/file/<int:file_pk>/',
         views.ManagedFileRetrieveUpdateDestroyGenericAPIView.as_view(),
         name='managed_file_create'),
])

urlpatterns = [
    path('', views.RepositoryListCreateGenericAPIView.as_view(), name='repository_list_create'),
    path('<int:pk>/',
         views.RepositoryRetrieveUpdateDestroyGenericAPIView.as_view(),
         name='repository_retrieve_update_destroy'),
    path('<int:repository_pk>/directory/<int:dir_pk>/', include(file_patterns))
]
