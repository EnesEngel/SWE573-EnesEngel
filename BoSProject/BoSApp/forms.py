from django import forms
from .models import UserProfile

'''
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'is_private']

    def clean_password(self):
        password = self.cleaned_data['password']
        return password
'''
