from django.core.validators import URLValidator
from django.db import models
from accounts.models import Company
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

Employee = get_user_model()


class TaskType(models.Model):
    class Meta:
        db_table = "task_type"
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="task_types")
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(max_length=512, blank=False)
    created_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="tasks_created_by")


class Task(models.Model):
    class Meta:
        db_table = "task"
    title = models.CharField(blank=False, null=False, max_length=56)
    task_type = models.ForeignKey(TaskType, on_delete=models.PROTECT, related_name="tasks")
    assigned_for = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="tasks_company")
    assigned_to = models.ManyToManyField(Employee, related_name="task_assigned_to")
    assigned_by = models.ManyToManyField(Employee, related_name="task_assigned_by")
    cc = models.ManyToManyField(Employee, related_name="task_cc")
    created_by = models.ForeignKey(TaskType, on_delete=models.PROTECT, related_name="tasks_created_by")
    created_on = models.DateTimeField(_('date created'), auto_now_add=True)
    assigned_on = models.DateTimeField(_('date assigned'), blank=False)
    description = models.TextField(max_length=1000)
    close_date = models.DateTimeField(_('closing date'), blank=True)
    update_on = models.DateTimeField(_('closing date'), auto_now=True, blank=True)


class TaskDocuments(models.Model):
    class Meta:
        db_table = "task_document"
    document_name = models.CharField(max_length=100, blank=False, null=False)
    document_link = models.TextField(validators=[URLValidator()])
    task = models.ForeignKey(Task, related_name='document_tasks', on_delete=models.PROTECT)
    created_by = models.ForeignKey(Employee, related_name='document_created_by', on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)


class CompletionHour(models.Model):
    class Meta:
        db_table = "completion_hrs"
    task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name="completion_hours")
    completed_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="completion_hours_by")
    completed_on = models.DateTimeField(_('completion date'))
    completion_hours = models.IntegerField(_('hours'))
    completion_minutes = models.IntegerField(_('minutes'))


class Comment(models.Model):
    class Meta:
        db_table = "comment"
    task = models.ForeignKey(Task, on_delete=models.PROTECT, related_name="comments")
    comment_by = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="comments_by")
    comment_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000)
