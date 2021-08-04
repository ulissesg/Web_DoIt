from django.urls import path

from . import views

app_name = 'DoIt'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tasks/<int:pk>', views.ListTasksView.as_view(), name='tasks'),
    path('task/<int:pk>', views.DetailsTaskView.as_view(), name='details'),
    path('new-list/', views.NewListView.as_view(), name='new_list'),
    path('new-task/<int:pk>', views.NewTaskView.as_view(), name='new_task'),
    path('delete-list/<int:pk>', views.ListDeleteView.as_view(), name='list_delete'),
    path('delete-task/<int:pk>', views.TaskDeleteView.as_view(), name='task_delete'),
    path('edit-list/<int:pk>', views.ListEditView.as_view(), name='list_edit'),
    path('edit-task/<int:pk>', views.TaskEditView.as_view(), name='task_edit'),
    path('sign-up/', views.NewUserView.as_view(), name='signup')

]
