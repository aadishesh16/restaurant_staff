from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import NewUser,JobPosting, Restaurant,JobApplication
class UserRegisterForm(UserCreationForm):
	
	class Meta:
		model = NewUser
		fields = ['username','email','password1','password2','restaurant','restaurant_admin','location']


class ManagerRegisterForm(UserCreationForm):


    location = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
	    model = NewUser
	    fields = ['username','email','password1','password2','location','hiring_manager']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].choices= [(loc.location, loc.location) for loc in Restaurant.objects.all()]

class JobPost(forms.ModelForm):
	# locat = Restaurant.objects.values_list('location', flat=True).distinct()
	# print(locat)
	# Restaurant.objects.invalidate(locat)
	# query_choices = [('', 'None')] + [(loc, loc) for loc in locat]
	# location = forms.ChoiceField(choices=query_choices, widget=forms.Select())
    location = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
    	model = JobPosting

    	fields = ['title','description','location']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].choices= [(loc.location, loc.location) for loc in Restaurant.objects.all()]


class LocationPost(forms.ModelForm):
	class Meta:
		model = Restaurant
		fields = ['location']

class JobApply(forms.ModelForm):
	class Meta:
		model = JobApplication
		fields = ['job_user','job_file']
