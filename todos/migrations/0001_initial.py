# Generated by Django 2.2 on 2020-02-10 11:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=56)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('assigned_on', models.DateTimeField(verbose_name='date assigned')),
                ('description', models.TextField(max_length=1000)),
                ('close_date', models.DateTimeField(blank=True, verbose_name='closing date')),
                ('update_on', models.DateTimeField(auto_now=True, verbose_name='closing date')),
                ('assigned_by', models.ManyToManyField(related_name='task_assigned_by', to=settings.AUTH_USER_MODEL)),
                ('assigned_for', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_company', to='accounts.Company')),
                ('assigned_to', models.ManyToManyField(related_name='task_assigned_to', to=settings.AUTH_USER_MODEL)),
                ('cc', models.ManyToManyField(related_name='task_cc', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=512)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='task_types', to='accounts.Company')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'task_type',
            },
        ),
        migrations.CreateModel(
            name='TaskDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(max_length=100)),
                ('document_link', models.TextField(validators=[django.core.validators.URLValidator()])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='document_created_by', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='document_tasks', to='todos.Task')),
            ],
            options={
                'db_table': 'task_document',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_created_by', to='todos.TaskType'),
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='todos.TaskType'),
        ),
        migrations.CreateModel(
            name='CompletionHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_on', models.DateTimeField(verbose_name='completion date')),
                ('completion_hours', models.IntegerField(verbose_name='hours')),
                ('completion_minutes', models.IntegerField(verbose_name='minutes')),
                ('completed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='completion_hours_by', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='completion_hours', to='todos.Task')),
            ],
            options={
                'db_table': 'completion_hrs',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_on', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(max_length=1000)),
                ('comment_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments_by', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to='todos.Task')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
    ]
