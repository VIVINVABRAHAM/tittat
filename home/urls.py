from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('categories',views.categories),
    path('about',views.about),
    path('faq',views.faq),
    path('contact',views.contact),
    path('all_product',views.all_product),
    path('popular_products',views.popular_products),
    path('featured_products',views.featured_products),
    path('guest_query',views.guest_query),
    path('advertise',views.advertise),
    path('signup',views.signup),
    path('signin',views.signin),
    path('postsign',views.postsign),
    path('postsignup',views.postsignup),
    path('adver',views.adver),
    path('myadver',views.myadver),
    path('adpos/<da>/<am>',views.adpos),
    path('profile',views.profile),
    path('myprofile',views.myprofile),
    path('post_profile',views.post_profile),
    path('contact',views.contact),
    path('ad_myads',views.ad_myads),
    path('ad_mprofile',views.ad_mprofile),






    path('paying/',views.paying),
    path('paying/paymenthandler/', views.paymenthandler, name='paymenthandler'),













]