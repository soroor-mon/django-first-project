from django import forms
from taskManager.models import Task


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']

    def save(self, commit=True):
        instance = super(CreateTaskForm, self).save(commit=False)

        if commit:
            instance.save()
            self.save_m2m()

        return instance
