from django.urls import path
from . import views

urlpatterns = [
    path('', views.ParserDemoView.as_view(), name='json_parser'),
    path('parse/', views.ParseJSONAjaxView.as_view(), name='parse_json'),
]
