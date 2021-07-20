# Create your views here.
from django.views import generic

from DoIt.models import List, Task


class IndexView(generic.ListView):
    template_name = 'DoIt/index.html'
    context_object_name = 'list_of_lists'

    def get_queryset(self):
        return List.objects.all()


class ListTasksView(generic.ListView):
    template_name = 'DoIt/list_tasks.html'
    context_object_name = 'task_of_list'

    def get_queryset(self):
        return Task.objects.filter(list=self.kwargs.get('pk'))


class DetailsTaskView(generic.DetailView):
    model = Task
    template_name = 'DoIt/task_details.html'
