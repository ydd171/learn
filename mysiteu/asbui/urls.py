from django.urls import path
from django.contrib import admin
from . import views
app_name = 'asbui'
urlpatterns = [
#    path('', views.index, name='index'),
# ex: /polls/
    path('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('historylog', views.historylog, name='historylog'),
]