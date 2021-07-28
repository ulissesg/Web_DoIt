# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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
    context_object_name = 'task_of_list'

    def get_queryset(self):
        return Task.objects.filter(list=self.kwargs.get('pk'))


def new_task(request, pk):
    if request.method == 'POST':
        pass

    else:
        context = {
            'list': List.objects.get(pk=pk),
        }
        return render(request, 'DoIt/new_task.html', context)


class DetailsTaskView(generic.DetailView):
    model = Task
    template_name = 'DoIt/task_details.html'
