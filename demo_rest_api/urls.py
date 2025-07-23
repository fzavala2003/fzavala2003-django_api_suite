from django.urls import path
from . import views
from .views import DemoRestApi, DemoRestApiItem

urlpatterns = [
   path("index/", views.DemoRestApi.as_view(), name="demo_rest_api_resources" ),
   path('<str:id>/', DemoRestApiItem.as_view(), name='demo-item')

]