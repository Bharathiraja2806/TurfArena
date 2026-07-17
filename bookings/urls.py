from django.urls import path
from . import views
app_name = "bookings"
urlpatterns = [path("new/<slug:slug>/", views.create_booking, name="create"), path("history/", views.history, name="history")]
