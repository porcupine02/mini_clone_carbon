from django.db import models
from django.contrib.auth import get_user_model
from forms.models import Subject, Forms, FormFields

User = get_user_model()

# Create your models here.

class Project(models.Model):
    title_th = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    keyword = models.JSONField() # List of VARCHAR(20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, related_name='teacher_project', on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='project_created', on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='project_updated', on_delete=models.CASCADE, null=True)

class FormSubmission(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, related_name='formsubmissions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    approve_by = models.ForeignKey(User, related_name='formsubmission_approver', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_by = models.ForeignKey(User, related_name='formsubmission_created', on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='formsubmission_updated', on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = ('project', 'form')

class FormFieldResponse(models.Model):
    form_submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE)
    form_field = models.ForeignKey(FormFields, on_delete=models.CASCADE, related_name='form_field_res',)
    value = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='form_uploads/', blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='response_created', on_delete=models.SET_NULL, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='response_updated', on_delete=models.SET_NULL, null=True)
    class Meta:
        unique_together = ('form_field', 'form_submission')
