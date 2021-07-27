# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import generic

from DoIt.models import List, Task


class IndexView(generic.ListView):
    template_name = 'DoIt/index.html'
    context_object_name = 'list_of_lists'

    def get_queryset(self):
        return List.objects.all()


class NewList(generic.CreateView):
    model = List
    fields = '__all__'
    success_url = reverse_lazy('DoIt:index')


class EditList(generic.UpdateView):
    model = List
    fields = '__all__'
    success_url = reverse_lazy('DoIt:index')


class DeleteList(generic.DeleteView):
    model = List
    success_url = reverse_lazy('DoIt:index')


class ListTasksView(generic.ListView):
    template_name = 'DoIt/list_tasks.html'
    context_object_name = 'tasks_of_list'

    def get_queryset(self):
        return Task.objects.filter(list=self.kwargs.get('pk'))


class NewTask(generic.CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('DoIt:index')


class EditTask(generic.UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('DoIt:index')

    def post(self, request, **kwargs):
        task = self.get_object()
        request.POST = request.POST.copy()
        request.POST['name'] = task.name
        request.POST['description'] = task.description
        request.POST['is_done'] = task.is_done
        request.POST['start_date'] = task.start_date
        request.POST['end_date'] = task.end_date
        request.POST['time_it_takes'] = task.time_it_takes
        request.POST['is_important'] = task.is_important
        return super(EditTask, self).post(request, **kwargs)


class DeleteTask(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('DoIt:index')


class DetailsTaskView(generic.DetailView):
    model = Task
    template_name = 'DoIt/task_details.html'
