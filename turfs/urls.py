from django.urls import path
from . import views
app_name = "turfs"
urlpatterns = [
    path("", views.turf_list, name="list"),
    path("manage/", views.manage_list, name="manage_list"),
    path("manage/add/", views.manage_create, name="manage_create"),
    path("manage/<int:pk>/edit/", views.manage_edit, name="manage_edit"),
    path("manage/<int:pk>/delete/", views.manage_delete, name="manage_delete"),
    path("<slug:slug>/", views.turf_detail, name="detail"),
]
