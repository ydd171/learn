from django.contrib import admin
from django.urls import path,include
from bsl import views
urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('add_job/', views.add_job),
    path('run_job/',views.run_job),
    path('index/',views.index),
    path('add_host/',views.add_host),
    path('job_list/',views.job_list),
    path('delete_job/',views.delete_job),
    path('edit_job/',views.edit_job),
    path('host_list/',views.host_list),
    path('edit_host/',views.edit_host),
    path('delete_host/',views.delete_host),
    path('history_list/',views.history_list),
    path('update/',views.update),
    path('add_upversion/',views.add_upversion),
    path('upversion_list/',views.upversion_list),
    path('ShowJob_update/',views.ShowJob_update),
]
