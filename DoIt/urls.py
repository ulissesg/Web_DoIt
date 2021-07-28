from django.urls import path

from . import views
from .views import IndexView

app_name = 'DoIt'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tasks/<int:pk>', views.ListTasksView.as_view(), name='tasks'),
    path('<int:pk>/', views.DetailsTaskView.as_view(), name='details'),
    path('new_list/', views.new_list, name='new_list'),
    path('new_task/<int:pk>', views.new_task, name='new_task'),
]
