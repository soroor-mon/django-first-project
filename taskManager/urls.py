from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from taskManager import views

app_name = 'taskManager'
urlpatterns = [

    path('', views.TaskListView.as_view(), name='all-task'),
    path('task/create', views.TaskCreateView.as_view(), name='create-task'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='detail-task'),
    path('task/update/<int:pk>', views.TaskUpdateView.as_view(), name='update-task'),
    path('task/delete/<int:pk>', views.TaskDeleteView.as_view(), name='delete-task'),

    path('api/task/', views.TaskList.as_view()),
    path('api/task/<int:pk>/', views.TaskDetail.as_view()),
    path('api/user/', views.UserList.as_view()),
    path('api/user/<int:pk>/', views.UserDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)