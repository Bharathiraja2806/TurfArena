from django.urls import path
from . import views

app_name = "payments"
urlpatterns = [
    path("checkout/<uuid:reference>/", views.checkout, name="checkout"),
    path("success/<uuid:reference>/", views.success, name="success"),
]
