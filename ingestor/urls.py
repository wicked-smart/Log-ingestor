from django.urls import path 
from . import views 

urlpatterns = [
    path("ingest", views.ingest, name="ingest"),
    path("query", views.query, name="query")

]

