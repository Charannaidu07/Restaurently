from django.urls import path
from . import views
#from .views import success_view
urlpatterns=[
    path('',views.index,name='index'),
    path('menu/',views.menu,name='menu'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('service/', views.service, name='service'),
    path('about/', views.about, name='about'),
    path('update_item/', views.updateItem, name='update_item'),
    path('booking/', views.booking, name='booking'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('contact/', views.contact, name='contact'),
    path('my_table/', views.my_table, name='my_table'),
    path('success/', views.success, name='success'),
    path('processOrder/', views.processOrder, name='processOrder'),
    path('logout/', views.logout, name='logout'),
]
