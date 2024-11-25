from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView

from .forms import ProjectForm, TaskForm, UserTaskForm, UserProjectForm
from .models import User, Project, Task, UserTask, UserProject, Message

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class LoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = '/login'
    
    def get(self, request, *args, **kwargs):
        if request.user.tipo != 'super':
            return redirect('project')
        
        context = self.get_context_data(**kwargs)
        context['user_type'] = request.user.tipo
        return self.render_to_response(context)


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'project.html'
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        project_id = kwargs.get('project_id')
        users_projects = UserProject.objects.filter(up_project=project_id)
        
        context['project_form'] = ProjectForm()
        context['task_form'] = TaskForm()
        context['user_project_form'] = UserProjectForm()
        user_task_form = UserTaskForm()
        user_task_form.fields['ut_user'].queryset = User.objects.filter(id__in=UserProject.objects.filter(up_project=project_id).values('up_user'))
        context['user_task_form'] = user_task_form

        context['project_id'] = project_id
        context['user_type'] = request.user.tipo
        
        if request.user.tipo in ['super']:
            context['projects'] = Project.objects.all()
        else:
            users_projects = UserProject.objects.filter(up_user=request.user.id)
            context['projects'] = Project.objects.filter(id__in=users_projects.values('up_project'))
        
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST)
        task_form = TaskForm(request.POST)
        user_project_form = UserProjectForm(request.POST)
        user_task_form = UserTaskForm(request.POST)
        project_id = kwargs.get('project_id')
        
        if 'deadline' in request.POST:
            project_instance = Project.objects.get(id=project_id)
            if task_form.is_valid():
                # Salva os dados da task
                task_form = task_form.save(commit=False)
                task_form.project = project_instance
                task_form.save()
                try:
                    return redirect('project_id', project_id=project_id)
                except:
                    return redirect('project')

            
        elif 'up_user' in request.POST:
            if user_project_form.is_valid():
                user_project_form.save()

            try:
                return redirect('project_id', project_id=project_id)
            except:
                return redirect('project')
        
        elif 'ut_user' in request.POST:
            if user_task_form.is_valid():
                user_task_form.save()

            try:
                return redirect('project_id', project_id=project_id)
            except:
                return redirect('project')
        
        else:
            if project_form.is_valid():
                # Salva o formulário de projeto
                project_form.save()
            try:
                return redirect('project_id', project_id=project_id)
            except:
                return redirect('project')

        # Caso não seja válido, renderize novamente a página
        context = self.get_context_data(**kwargs)
        context['project_form'] = project_form
        context['task_form'] = task_form
        context['user_project_form'] = user_project_form
        return self.render_to_response(context)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.all()
        status = {'pending': 'Pendente', 'in_progress': 'Em Progresso', 'completed': 'Finalizada'}

        for task in tasks:
            task.status = status[task.status]
        
        context['tasks'] = tasks

        return context


@csrf_exempt
def update_task(request, task_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            field = list(data.keys())[0]
            value = data[field]

            # Validação para o campo de status
            if field == 'status':
                valid_statuses = dict(Task.STATUS_CHOICES).keys()
                if value not in valid_statuses:
                    return JsonResponse({'status': 'error', 'message': 'Status inválido'}, status=400)

            # Atualiza o campo no banco de dados
            task = Task.objects.get(id=task_id)
            setattr(task, field, value)
            task.save()

            return JsonResponse({'status': 'success', 'message': 'Tarefa atualizada com sucesso'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)


@csrf_exempt
def chat_messages(request, task_id):
    if request.method == 'GET':
        # Recuperar mensagens do projeto
        messages = Message.objects.filter(task=task_id).order_by('timestamp')
        data = [
            {
                'sender': msg.sender.first_name,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for msg in messages
        ]
        return JsonResponse({'messages': data})

    elif request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        task = Task.objects.get(id=task_id)
        if not content:
            return JsonResponse({'error': 'Message content is required'}, status=400)

        try:
            Message.objects.create(
                sender=request.user,
                task=task,
                content=content
            )
            return JsonResponse({'status': 'success'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
