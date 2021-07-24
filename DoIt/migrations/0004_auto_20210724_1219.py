# Generated by Django 3.2.5 on 2021-07-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DoIt', '0003_alter_task_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='is_done',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='is_important',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_it_takes',
            field=models.IntegerField(blank=True, null=True, verbose_name='How much time it takes'),
        ),
    ]
