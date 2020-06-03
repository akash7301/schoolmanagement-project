"""BlogProjectTwo URL Configuration

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
from django.urls import path
from django.conf.urls import url,include
from blog import views

urlpatterns = [
    path('base/',views.index,name='base'),
    path('admin/', admin.site.urls),
    path('signup/',views.sign_up_view,name='signup'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('test/',views.post_list_view,name='post_list'),
    path('tag/<str:tag_slug>/',views.post_list_view,name='post_list_by_tag_name'),
    path('<int:year>/<int:month>/<int:day>/<str:post>/',views.post_detail_view,name='post_detail'),
    path('<int:id>/',views.mail_send_view),
    path('addpost/',views.add_post_view,name='addpost'),
    path('post_list_full/',views.post_list_full_view,name='post_list_full'),

    url(r'^search_p/',views.search_post,name='search_p'),
]
