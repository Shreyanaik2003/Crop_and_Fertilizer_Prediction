from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('register',views.register,name='reg'),
    path('login',views.login,name='login'),
    path('data',views.data,name='data'),
    path('predict',views.predict,name='predict'),
    path('logout',views.logout,name='logout')
]