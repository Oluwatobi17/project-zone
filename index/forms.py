from django import forms
from .models import User, Project, Contact


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username','email', 'password']

class EditProfileForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['first_name','last_name','phonenum','email','nationality','about','job_description','job_title','contact_address']


class EditPicsForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['resume','profilePics']

class ProjectPicForm(forms.ModelForm):

	class Meta:
		model = Project
		fields = ['picture']

class CreateProjectForm(forms.ModelForm):

	class Meta:
		model = Project
		fields = ['title','short_desc', 'full_desc', 'user']


class EditProjectForm(forms.ModelForm):

	class Meta:
		model = Project
		fields = ['title','short_desc', 'full_desc']


class ContactForm(forms.ModelForm):

	class Meta:
		model = Contact
		fields = ['name','message', 'email']

