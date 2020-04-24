"""unica_UI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages import views
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'pages.views.handler404'
handler500 = 'pages.views.handler500'
urlpatterns = [
    path('unica/', include('pages.urls') ),
    path('loadjsonindb', views.loadjsonindb),
    path('dbtable', views.dbtable),
    path('dbtable_latest', views.dbtable_latest),
    path('dbtable_date',views.dbtable_info),
    path('',include('accounts.urls')),
    path('testlab1_logfile',views.testlab1_logfile),
    path('testlab2_logfile',views.testlab2_logfile),
    path('ajax-post', views.ajax),
    path('admin/', admin.site.urls),
    path('sample_report',views.sample_report),
    path('adhoc',views.adhoc),
    path('execute1',views.execute1),
    path('execute1_result',views.execute1_result),
    path('logpoller',views.logpoller),
    path('failed_positive',views.failed_positive),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
