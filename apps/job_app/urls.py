from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'dashboard/new$', views.new),
    url(r'^create_job$', views.create_job),
    url(r'edit_form/(?P<job_id>\d+)$',views.edit_form),
    url(r'editing/(?P<job_id>\d+)$',views.editing),
    url(r'^remove/(?P<job_id>\d+)$', views.remove),
    url(r'^details/(?P<job_id>\d+)$', views.details),

]