# Create your views here.
import form as form
from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.widgets import AdminDateWidget
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.template import loader
from django.template.defaultfilters import default
from django.urls import reverse, reverse_lazy
from django.utils.dateformat import DateFormat
from django.views import generic

from DoIt.models import List, Task


class IndexView(generic.ListView):
    template_name = 'DoIt/index.html'
    context_object_name = 'list_of_lists'

    def get_queryset(self):
        return List.objects.all()


class ListTasksView(generic.ListView):
    template_name = 'DoIt/list_tasks.html'
    context_object_name = 'list_of_task'

    def get_queryset(self):
        return Task.objects.filter(list=self.kwargs.get('pk'))


class NewListView(SuccessMessageMixin, generic.CreateView):
    model = List
    fields = '__all__'

    def get_success_url(self):
        messages.info(self.request, 'List ' + self.request.POST['name'] + ' created successfully')
        return reverse_lazy('DoIt:index')

    def get_context_data(self, **kwargs):
        context = super(NewListView, self).get_context_data(**kwargs)
        context['page_title'] = 'New List'
        return context


class ListEditView(SuccessMessageMixin, generic.UpdateView):
    model = List
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ListEditView, self).get_context_data(**kwargs)
        context['page_title'] = 'Edit List ' + get_object_or_404(List, id=self.kwargs['pk']).name
        return context

    def get_success_url(self):
        messages.info(self.request, 'List ' + self.request.POST['name'] + ' Edited')
        return reverse_lazy('DoIt:index')


class ListDeleteView(generic.DeleteView):
    model = List
    success_url = reverse_lazy('DoIt:index')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'is_done', 'start_date', 'end_date', 'time_it_takes', 'is_important')
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class NewTaskView(SuccessMessageMixin, generic.CreateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        messages.info(self.request, 'Task ' + self.request.POST['name'] + ' created successfully')
        return reverse_lazy('DoIt:tasks', kwargs={
            'pk': self.kwargs['pk']
        })

    def form_valid(self, form):
        lst = get_object_or_404(List, id=self.kwargs['pk'])
        form.instance.list = lst
        return super(NewTaskView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NewTaskView, self).get_context_data(**kwargs)
        context['list'] = get_object_or_404(List, id=self.kwargs['pk'])
        context['page_title'] = 'Adding a new task to the list'
        return context


class DetailsTaskView(generic.DetailView):
    model = Task
    template_name = 'DoIt/task_details.html'


class TaskEditView(SuccessMessageMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm

    def get_success_url(self):
        messages.info(self.request, 'Task ' + self.request.POST['name'] + ' edited')
        return reverse_lazy('DoIt:tasks', kwargs={'pk': get_object_or_404(Task, id=self.kwargs['pk']).list.id})

    def get_context_data(self, **kwargs):
        context = super(TaskEditView, self).get_context_data(**kwargs)
        context['list'] = get_object_or_404(List, id=get_object_or_404(Task, id=self.kwargs['pk']).list.id)
        context['page_title'] = 'Editing task of'
        return context


class TaskDeleteView(generic.DeleteView):
    model = Task

    def get_success_url(self):
        task = get_object_or_404(Task, id=self.kwargs['pk'])
        messages.info(self.request, 'Task ' + task.name + ' deleted successfully')
        return reverse_lazy('DoIt:tasks', kwargs={
            'pk': task.list.id
        })
