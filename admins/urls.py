from django.urls import path
from . import views

urlpatterns=[
    path('admin_sign',views.admin_sign),
    path('logout',views.logout,name='logg'),
    path('postadminsg',views.postadminsg),
    path('admin_home',views.admin_home),
    path('admin_deactive',views.admin_deactive),
    path('admin_approved',views.admin_approved),
    path('admin_processing',views.admin_processing),
    path('admin_user',views.admin_user),
    path('admin_evaluator',views.admin_evaluator),
    path('admin_demand',views.admin_demand),
    path('admin_pro_details/<pid>/<uid>',views.admin_pro_details),
    path('way_approve/<pid>/<uid>',views.way_approve),
    path('admin_products',views.admin_products),
    path('user_delete/<uid>',views.user_delete),

    path('admin_ads',views.admin_ads),
    path('admin_approve/<uid>/<pid>',views.admin_approve),
    path('ad_approve/<uid>/<pid>',views.ad_approve),






]
