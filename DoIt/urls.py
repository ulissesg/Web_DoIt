from django.urls import path

from . import views

app_name = 'DoIt'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.ListTasksView.as_view(), name='tasks'),
    path('detail/<int:pk>', views.DetailsTaskView.as_view(), name='details'),
    path('new_list/', views.NewList.as_view(), name='new_list'),
    path('new_task/', views.NewTask.as_view(), name='new_task'),
    path('delete_list/<int:pk>', views.DeleteList.as_view(), name='delete_list'),
    path('delete_task/<int:pk>', views.DeleteTask.as_view(), name='delete_task'),
    path('edit_list/<int:pk>', views.EditList.as_view(), name='edit_list'),
    path('edit_task/<int:pk>', views.EditTask.as_view(), name='edit_task')
]
