from django.urls import path

from taskManager import views

app_name = 'taskManager'
urlpatterns = [
    path('', views.TaskListView.as_view(), name='all-task'),
    path('task/create', views.TaskCreateView.as_view(), name='create-task'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='detail-task'),
    path('task/update/<int:pk>', views.TaskUpdateView.as_view(), name='update-task'),
    path('task/delete/<int:pk>', views.TaskDeleteView.as_view(), name='delete-task'),
    
]
