
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('search/', include('search.urls')),
    path('accounts/', include('accounts.urls')),
    path('feedbacks/', include('feedbacks.urls')),
]
