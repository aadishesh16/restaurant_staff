from django.urls import path
from . import views 
from .views import (PostCreateView,
	JobListView,
	JobDetailView,
	InternalJobListView,
	JobApplyListView,
	AdminJobListView,
	JobUpdateView,
	LocationUpdateView,
	LocationDeleteView,
	JobPostDeleteView)
urlpatterns = [
	path('',views.home,name="home"),
    path('staffregister/', views.register, name="staff-register"),
    path('managerregister/', views.register_manager, name="manager-register"),
    path('internaljobpost/', InternalJobListView.as_view(), name="internaljobposting"),
    path('home/', views.home, name="home"),
    path('addlocation/', views.add_location, name="location-add"),
    path('jobposting/', views.create_view, name="postcreate"),
    path('joblist/', JobListView.as_view(), name="joblist"),
    path('joblist/<int:pk>', JobDetailView.as_view(), name="joblist-detail"),
    path('applicationlist/<int:pk>', JobApplyListView.as_view(), name="job-application"),
    path('reject/<int:pk>', views.rejectapplication, name="job-reject"),
    path('accept/<int:pk>', views.acceptapplication, name="job-accept"),
    path('adminjobpost/', AdminJobListView.as_view(), name="adminjobpost"),
    path('adminlocation/', views.restlocation, name="adminlocation"),
    path('updatejobpost/<int:pk>', JobUpdateView.as_view(), name="adminjobupdate"),
    path('updatelocation/<int:pk>', LocationUpdateView.as_view(), name="location-update"),
    path('deletelocation/<int:pk>', LocationDeleteView.as_view(), name="location-delete"),
    path('deletejob/<int:pk>', JobPostDeleteView.as_view(), name="job-delete"),







]
