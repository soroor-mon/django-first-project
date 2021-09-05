from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.
from django.conf import settings

STARTED_STATUS = 1
PROCESSING_STATUS = 2
PENDING_STATUS = 3
ENDED_STATUS = 4
STATUS_CHOICES = (
        (STARTED_STATUS, 'Started'),
        (PROCESSING_STATUS, 'Processing'),
        (PENDING_STATUS, 'Pending'),
        (ENDED_STATUS, 'Ended')
    )


class Task(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2, "Task title must be greater than 1 character")]
    )
    description = models.CharField(
        max_length=2000,
        validators=[MinLengthValidator(2, "Project description must be greater than 1 character")]
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=STARTED_STATUS)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
