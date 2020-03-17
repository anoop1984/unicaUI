from django.urls import path
from . import views

urlpatterns = [
    path('about', views.about, name='about'),
    #path('', views.index,name='index'),
    path('testlab1',views.index2, name='testlab1'),
    path('testlab2', views.testlab2, name='testlab2')
]
