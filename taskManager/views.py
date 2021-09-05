from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView

from taskManager.forms import CreateTaskForm
from taskManager.models import Task
from django.views import View


class TaskListView(View):
    model = Task

    def get(self, request):
        strval = request.GET.get("search", False)
        if strval:
            query = Q(description__contains=strval) | Q(title__contains=strval)
            task_list = Task.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else:
            task_list = Task.objects.all()
        ctx = {'task_list': task_list, 'search': strval}
        return render(request, "taskManager/task_list.html", ctx)


class TaskCreateView(View):
    model = Task
    template_name = 'taskManager/task_form.html'

    def get(self, request, pk=None):
        form = CreateTaskForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateTaskForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        task = form.save(commit=False)
        task.owner = self.request.user
        task.save()
        form.save_m2m()

        return HttpResponseRedirect(reverse('taskManager:all-task'))


class TaskDetailView(View):
    model = Task

    def get(self, request, pk):
        x = get_object_or_404(Task, id=pk)
        ctx = {'task': x}
        return render(request, "taskManager/task_detail.html", ctx)


class TaskUpdateView(LoginRequiredMixin, View):
    model = Task
    template_name = 'taskManager/task_form.html'

    def get(self, request, pk=None):
        task = get_object_or_404(Task, id=pk, owner=self.request.user)
        form = CreateTaskForm(instance=task)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        task = get_object_or_404(Task, id=pk, owner=self.request.user)
        form = CreateTaskForm(request.POST, instance=task or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        task = form.save(commit=False)
        task.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse('taskManager:all-task'))


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def get_success_url(self):
        return reverse('taskManager:all-task')
