from django.urls import path 
from . import views 

urlpatterns = [
    path("ingest", views.ingest, name="ingest")

]

