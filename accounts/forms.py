from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

Employee = get_user_model()


class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'email', 'dob', 'bio', 'phone_number', 'alternate_email')
        field_classes = {'username': UsernameField}
