from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, IndexView, ProjectView, update_task, chat_messages, DeleteTask

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('', IndexView.as_view(), name='index'),
    path('update-task/<int:task_id>/', update_task, name='update_task'),
    path('project/', ProjectView.as_view(), name='project'),
    path('project/<int:project_id>', ProjectView.as_view(), name='project_id'),
    path('chat/<int:task_id>/', chat_messages, name='chat_messages'),

    path('delete-task/<int:pk>/<int:project_id>/', DeleteTask.as_view(), name='delete_task'),
]