from django.conf.urls import url

from . import views

urlpatterns = [
    # render routes
    url(r"^$", views.index, name="index"),
    url(r"jobs/new$", views.new_job, name="new_job"),
    url(r"jobs/(?P<job_id>\d+)$", views.view_job, name="view_job"),
    url(r"jobs/edit/(?P<job_id>\d+)$", views.edit_job, name="edit_job"),
    # process routes
    url(r"register$", views.register, name="reg"),
    url(r"login$", views.login, name="login"),
    url(r"logout$", views.logout, name="logout"),
    url(r"process_job$", views.process_job, name="process_job"),
    url(r"process_edit$", views.process_edit, name="process_edit"),
    url(r"accept/(?P<job_id>\d+)$", views.accept, name="accept"),
    url(r"give_up/(?P<job_id>\d+)$", views.give_up, name="give_up"),
    url(r"destroy/(?P<job_id>\d+)$", views.destroy, name="delete_job"),
]
