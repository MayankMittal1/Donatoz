"""Donatoz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from donate import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('signup', views.signup),
    path('login_check_u', views.login_user,name="login_user"),
    path('login_check_0', views.login_organization,name="login_organization"),
    path('register_u', views.registerUser,name="register_user"),
    path('register_o', views.registerOrganization,name="register_organization"),
    path('certificate/<str:id>/', views.render_pdf_view),
    path('home',views.home,name='home'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('donate',views.donate,name='donate'),
    path('donate/<str:id>/',views.transact,name='donate'),
    path('donate/search',views.searchOrganization,name='donate'),
    path('transactions/add',views.addTransaction,name='add'),

]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
