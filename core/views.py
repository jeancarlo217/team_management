from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView

from .forms import ProjectForm, TaskForm, UserTaskForm, UserProjectForm
from .models import User, Project, Task, UserTask, UserProject

class LoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = '/login'


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'project.html'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        project_id = kwargs.get('project_id')
        context['project_form'] = ProjectForm()
        context['task_form'] = TaskForm()
        context['user_project_form'] = UserProjectForm()
        context['users'] = User.objects.all()
        context['project_id'] = project_id
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST)
        task_form = TaskForm(request.POST)
        project_id = kwargs.get('project_id')
        
        if 'deadline' not in request.POST:
            if project_form.is_valid():
                # Salva o formulário de projeto
                project_form.save()
                return redirect('project')
        else:
            if task_form.is_valid():
                project_instance = Project.objects.get(id=project_id)
                # Salva os dados da task
                task_form = task_form.save(commit=False)
                task_form.project = project_instance
                task_form.save()

                # Cria relação entre task e project
                user_task_form = UserTaskForm(data={
                    'user': project_id,
                    'task': task_form.id,
                })

                if user_task_form.is_valid():
                    user_task_form.save()
                    return redirect('project_id', project_id=project_id)

        # Caso não seja válido, renderize novamente a página
        context = self.get_context_data(**kwargs)
        context['project_form'] = project_form
        context['task_form'] = task_form
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        # Corrigindo chamada ao método pai
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['tasks'] = Task.objects.all()
        return context
