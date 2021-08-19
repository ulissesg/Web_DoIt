# Create your views here.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from DoIt.models import List, Task


class IndexView(generic.ListView):
    template_name = 'DoIt/index.html'
    context_object_name = 'list_of_lists'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return List.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.request.user.is_authenticated:
            context = super(IndexView, self).get_context_data(**kwargs)
            context['user'] = self.request.user
            return context


class ListTasksView(generic.ListView):
    template_name = 'DoIt/list_tasks.html'
    context_object_name = 'list_of_task'

    def get_queryset(self):
        return Task.objects.filter(list=self.kwargs.get('pk'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListTasksView, self).get_context_data(**kwargs)
        tasks = context['list_of_task']
        total = 0
        for task in tasks:
            total = total + int(task.time_it_takes or 0)
        context['time_finish_list'] = total
        return context


class NewListView(SuccessMessageMixin, generic.CreateView):
    model = List
    fields = ('name',)

    def get_success_url(self):
        messages.info(self.request, 'List ' + self.request.POST['name'] + ' created successfully')
        return reverse_lazy('DoIt:index')

    def get_context_data(self, **kwargs):
        context = super(NewListView, self).get_context_data(**kwargs)
        context['page_title'] = 'New List'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NewListView, self).form_valid(form)


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

    def get_success_url(self):
        messages.info(self.request,
                      'List ' + get_object_or_404(List, id=self.kwargs['pk']).name + ' deleted successfully')
        return reverse_lazy('DoIt:index')


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


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class NewUserView(SuccessMessageMixin, generic.CreateView):
    model = User
    success_url = reverse_lazy('login')
    form_class = NewUserForm

    def get_context_data(self, **kwargs):
        context = super(NewUserView, self).get_context_data(**kwargs)
        context['page_title'] = 'New User'
        return context

    def get_success_message(self, cleaned_data):
        return 'User ' + self.request.POST['username'] + ' Added'
