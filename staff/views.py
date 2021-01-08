from django.shortcuts import render,redirect
from .forms import UserRegisterForm,JobPost,LocationPost,ManagerRegisterForm,JobApply
from .models import JobPosting, JobApplication, Restaurant
from django.views.generic import CreateView, ListView, DetailView,UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls  import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages


# Create your views here.
@login_required
def register(request):
	if request.user.is_superuser ==True:
		if request.method=="POST":
			form = UserRegisterForm(request.POST)
			if form.is_valid():
				form.save()
				username= form.cleaned_data.get('username')
				return redirect("home")
		else:
			form= UserRegisterForm()
	else:
		return redirect('home')
	return render(request,'staff/registration.html', {'form':form})

def home(request):
	if request.user.is_authenticated==True:

		return render(request,'staff/home.html')
	else:
		return redirect('login')




class JobListView(ListView):
	model = JobPosting
	template_name = "staff/jobportal.html"
	context_object_name='jobs'
	ordering = ['-date_posted']
	paginate_by=5


class InternalJobListView(ListView):
	model = JobPosting
	template_name = "staff/internaljoblist.html"
	context_object_name='jobs'
	def get_queryset(self):
		queryset = JobPosting.objects.filter(restaurant=self.request.user.restaurant).filter(location=self.request.user.location)

		return queryset
	paginate_by=5


class JobDetailView(DetailView):
	model = JobPosting



# class UserAccessMixin(PermissionRequiredMixin):
# 	def dispatch(self,request,*args,**kwargs):
# 		if not self.request.user.restaurant_Admin:
# 			return redirect('home')
# 		if not self.has_permission():
# 			return redirect('home')
# 		return super(UserAccessMixin,self).dispatch(request,*args,**kwargs)
@login_required
def create_view(request):
	if request.user.restaurant_admin ==True:
		if request.method=="POST":
			form = JobPost(request.POST)
			if form.is_valid():
				form.instance.user = request.user
				form.instance.restaurant= request.user.restaurant
				form.save()
				return redirect("home")
		else:
			form= JobPost()
	else:
		return redirect('home')
	return render(request,'staff/jobposting_form.html', {'form':form})



class PostCreateView(LoginRequiredMixin,CreateView):

	model = JobPosting
	fields = ['title','description']
	def form_valid(self,form):

		form.instance.user = self.request.user
		form.instance.location = self.request.user.location
		return super().form_valid(form)
		




@login_required
def add_location(request):
	if request.user.restaurant_admin ==True:
		if request.method=="POST":
			form = LocationPost(request.POST)
			if form.is_valid():
				form.instance.rest_user = request.user
				form.instance.rest_name = request.user.restaurant
				form.save()
				return redirect("home")
		else:
			form= LocationPost()
	else:
		return redirect('home')
	return render(request,'staff/add_location.html', {'form':form})

@login_required
def register_manager(request):
	if request.user.restaurant_admin ==True:
		if request.method=="POST":
			form = ManagerRegisterForm(request.POST)
			if form.is_valid():
				form.instance.restaurant = request.user.restaurant
				form.save()

				return redirect("home")
		else:
			form= ManagerRegisterForm()
	else:
		return redirect('home')

	return render(request,'staff/managerregistration.html', {'form':form})


def jobapply(request,pk):
	job = JobPosting.objects.filter(id=pk).first()
	if request.method=="POST":
		form = JobApply(request.POST,request.FILES)
		if form.is_valid():
			form.instance.job_desc = job
			form.save()
			return redirect("joblist")
	else:
		form = JobApply()
	return render(request,'staff/apply.html', {'form':form})

class JobApplyListView(ListView):
	model = JobApplication
	template_name = "staff/jobapplylist.html"
	context_object_name='jobs'
	def get_queryset(self):
		queryset = JobApplication.objects.filter(job_desc__restaurant=self.request.user.restaurant).filter(job_desc__location=self.request.user.location).filter(job_desc__id = self.kwargs['pk']).order_by('id')

		return queryset
	paginate_by =5


def rejectapplication(request,pk):
	application = JobApplication.objects.filter(id=pk).first()
	send_mail("Regarding your application",
		"We're sorry your application is not approved. Best wishes!",
		'aadishesharma@gmail.com',
		[application.job_user]
		)
	return redirect('internaljobposting')

def acceptapplication(request,pk):
	application = JobApplication.objects.filter(id=pk).first()
	val = pk
	send_mail("Regarding your application",
		"Congratulations your application has been approved! We'll contact you soon!",
		'aadishesharma@gmail.com',
		[application.job_user]
		)
	return redirect('internaljobposting')




class AdminJobListView(LoginRequiredMixin,ListView):
	model = JobPosting
	template_name = "staff/adminjoblist.html"
	context_object_name='jobs'
	ordering = ['-date_posted']
	paginate_by =5

	def get_queryset(self):
		queryset = JobPosting.objects.filter(user=self.request.user)


		return queryset
@login_required
def restlocation(request):
	queryset = Restaurant.objects.filter(rest_user=request.user)
	context = {'rest':queryset}
	if queryset:
		return render(request,'staff/restaurant.html',context)
	else:
		messages.error(request,f'Either you have not added locations or not authorized to view the page')
		return redirect('home')


# class RestLocationListView(LoginRequiredMixin,ListView):
# 	model = Restaurant
# 	template_name = "staff/restaurant.html"
# 	context_object_name='rest'


# 	def render_to_response(self, context):

# 	    if not self.rest_user:
# 	        return redirect('home')
# 	    return super(VideosView, self).render_to_response(context)

# 	def get_queryset(self):
# 		queryset = Restaurant.objects.filter(rest_user=self.request.user)
# 		return queryset
		

class JobUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = JobPosting
	template_name = "staff/jobupdate.html"
	fields = ['title','location','description']

	def test_func(self):
		update = self.get_object()
		if self.request.user == update.user:
			return True
		else:
			return False

	def form_valid(self,form):
		form.instance.user = self.request.user
		return super(JobUpdateView,self).form_valid(form)
	def get_success_url(self):
		return reverse('adminjobpost')


class LocationUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Restaurant
	template_name = "staff/locationupdate.html"
	fields = ['location']

	def test_func(self):
		update = self.get_object()
		if self.request.user == update.rest_user:
			return True
		else:
			return False

	def form_valid(self,form):
		form.instance.user = self.request.user
		form.instance.rest_name = self.request.user.restaurant
		return super().form_valid(form)
	def get_success_url(self):
		return reverse('adminlocation')


class LocationDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Restaurant
	success_url = reverse_lazy("adminlocation")
	def test_func(self):
		update = self.get_object()
		if self.request.user == update.rest_user:
			return True
		else:
			return False

class JobPostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = JobPosting
	template_name = "staff/deletejob.html"
	success_url = reverse_lazy("adminjobpost")
	def test_func(self):
		update = self.get_object()
		if self.request.user == update.user:
			return True
		else:
			return False