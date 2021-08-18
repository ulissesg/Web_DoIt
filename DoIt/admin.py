from django.contrib import admin

from DoIt.models import List, Task


class TaskInLine(admin.StackedInline):
    model = Task
    extra = 0
    fieldsets = ('task', {
        'classes': ('collapse',),
        'fields': ('name', 'description', 'is_done', 'start_date', 'end_date', 'time_it_takes', 'is_important'),
    }),


class ListAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'user']}),
    ]
    inlines = [TaskInLine]
    list_display = ('name', 'user')
    search_fields = ['name']


admin.site.register(List, ListAdmin)
