from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import DeleteView
from rest_framework import permissions, status, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from taskManager.forms import CreateTaskForm
from taskManager.models import Task
from django.views import View

from taskManager.serializers import TaskSerializer, UserSerializer


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


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


class TaskCreateView(LoginRequiredMixin, View):
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
        task = get_object_or_404(Task, id=pk, owner=request.user)
        form = CreateTaskForm(instance=task)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        task = get_object_or_404(Task, id=pk, owner=request.user)
        form = CreateTaskForm(request.POST, instance=task or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        task = form.save(commit=False)
        task.save()
        return HttpResponseRedirect(reverse('taskManager:all-task'))


# UserPassesTestMixin,
class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return self.object.owner == self.request.user

    def get_success_url(self):
        return reverse('taskManager:all-task')


class TaskList(APIView):
    """
    List all code tasks, or create a new task.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetail(APIView):
    """
    Retrieve, update or delete a code task instance.
    """
    #permission_classes = [AuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        self.permission_classes = [AuthorOrReadOnly]
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        self.permission_classes = [AuthorOrReadOnly]
        task = self.get_object(pk)
        #data = JSONParser().parse(request)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        self.permission_classes = [AuthorOrReadOnly]
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
