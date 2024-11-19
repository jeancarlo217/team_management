from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView

from .forms import ProjectForm, TaskForm
from .models import Project, Task

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
        context['project_form'] = ProjectForm()
        context['task_form'] = TaskForm()
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST)
        task_form = TaskForm(request.POST)
        
        if project_form.is_valid():
            project_form.save()
            return redirect('project')
        
        if task_form.is_valid():
            
            task_form.save()
            return redirect('project')
        
        context = self.get_context_data(**kwargs)
        context['project_form'] = project_form
        context['task_form'] = task_form
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['tasks'] = Project.objects.all()
        return context
