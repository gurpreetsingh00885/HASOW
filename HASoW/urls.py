
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from controller.views import CommandExecutor, HomeView, Controller, Renamer

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', auth_views.login, name='login', ),
    url(r'^logout/', auth_views.logout, name='logout', ),
    url(r'^logout_successful/', TemplateView.as_view(template_name="logout.html")),
    url(r'^home/', Controller.as_view()),
    url(r'^control/', Controller.as_view()),
    url(ur'^command/(?P<slug>.*)/$', CommandExecutor.as_view()),
    url(r'^rename/(?P<slug>.*)/$', Renamer.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
