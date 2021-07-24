# Create your views here.
from webbrowser import get

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.template import loader
from django.urls import reverse
from django.views import generic

from DoIt.models import List, Task


class IndexView(generic.ListView):
    template_name = 'DoIt/index.html'
    context_object_name = 'list_of_lists'

    def get_queryset(self):
        return List.objects.all()


def new_list(request):
    if request.method == 'POST':
        if request.POST['name']:
            list_name = request.POST['name']
            nw_list = List(name=list_name)
            nw_list.save()

            messages.info(request, 'List created successfully')
            return HttpResponseRedirect(reverse('DoIt:index'))

        else:
            # Redisplay the form to create a list.
            return render(request, 'DoIt/new_list.html', {
                'error_message': "You didn't typed a name for the list.",
            })

    else:
        template = loader.get_template('DoIt/new_list.html')
        return HttpResponse(template.render({}, request))


class ListTasksView(generic.ListView):
    template_name = 'DoIt/list_tasks.html'
    context_object_name = 'tasks_of_list'

    def get_queryset(self):
        return Task.objects.filter(list=self.kwargs.get('pk'))


def new_task(request, pk):
    if request.method == 'POST':
        # name is the only mandatory field to add a new task
        if request.POST['name']:
            task_name = request.POST['name']
            task_description = request.POST['description']
            task_is_done = True if request.POST.get('is_done') else False
            task_start_date = None if not request.POST['start_date'] else request.POST['start_date']
            print('startdate: ' + str(task_start_date))
            task_end_date = None if not request.POST['end_date'] else request.POST['end_date']
            print('end date: ' + str(task_end_date))
            task_time_it_takes = request.POST.get('time_it_takes', 0)
            task_is_important = True if request.POST.get('is_important') else False
            nw_task = Task(name=task_name, description=task_description, is_done=task_is_done,
                           start_date=task_start_date, end_date=task_end_date,
                           time_it_takes=task_time_it_takes, is_important=task_is_important,
                           list=get_object_or_404(List, pk=pk))
            nw_task.save()

            messages.info(request, 'Task created successfully')
            return HttpResponseRedirect(reverse('DoIt:tasks',
                                                kwargs={'pk': pk, 'name': get_object_or_404(List, pk=pk).name}))

        else:
            # Redisplay the form to create a task.
            return render(request, 'DoIt/new_task.html', {
                'list_name': get_object_or_404(List, pk=pk).name,
                'error_message': "You didn't typed a name for the task.",
            })

    else:
        context = {
            'list_name': get_object_or_404(List, pk=pk).name,
        }
        return render(request, 'DoIt/new_task.html', context)


class DetailsTaskView(generic.DetailView):
    model = Task
    template_name = 'DoIt/task_details.html'

