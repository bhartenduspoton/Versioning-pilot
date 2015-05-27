from django import forms
from django.contrib.auth.models import User
from main.models import  UserData,Project



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class UserDataForm(forms.ModelForm):
    Project_name = forms.ModelChoiceField(queryset=None,required=True,to_field_name="projectName")
    class Meta:
        model = UserData
        fields = ('Project_name','excelsheet','comments')

    def __init__(self, user, *args, **kwargs):
        #print user.username
        super(UserDataForm, self).__init__(*args, **kwargs)
        self.fields['Project_name'].queryset = Project.objects.values_list('projectName', flat=True).filter(user=user)
        #self.fields['Project_name'].queryset = Project.objects.filter(user=user)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('customerID','projectID','projectName')