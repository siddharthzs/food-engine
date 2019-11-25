
from django.contrib import admin
from django.urls import path , include
from django.views.generic.base import TemplateView
from django.conf.urls import url
from food import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('food/',views.foods, name='food'),
    path('food/<int:id>/', views.foods_delete, name='foods_delete'),
    path('<int:id>/', views.particular_food, name='particular_food'),

]
