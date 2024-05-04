"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from Myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Login),
    path('login_post',views.login_post),
    path('forgot_password',views.forgot_password),
    path('forgot_password_post',views.forgot_password_post),
    path('view_category',views.view_category),
    path('add_category',views.add_category),
    path('add_category_post',views.add_category_post),
    path('delete_category/<id>',views.delete_category),
    path('view_feedback',views.view_feedback),
    path('view_Customer',views.view_Customer),
    path('view_Seller',views.view_Seller),
    path('homepage',views.homepage),
    path('verified_sellers',views.verified_sellers),
    path('approve_seller/<id>',views.approve_seller),
    path('reject_seller/<id>',views.reject_seller),
    path('logout',views.logout),

    #.......................................................
    path('View_Product',views.View_Product),
    path('view_ratingss/<id>',views.view_ratingss),
    path('Sales_Report',views.Sales_Report),
    # path('Update_Status',views.Update_Status),
    path('View_Order',views.View_Order),
    path('view_profile',views.view_profile),
    path('Update_Product/<id>',views.Update_Product),
    path('Update_Product_post/<id>',views.Update_Product_post),
    path('Product_Add',views.Product_Add),
    path('Product_Add_post',views.Product_Add_post),
    path('Home_Page',views.Home_Page),
    path('Delete_Product/<id>',views.Delete_Product),
    path('update_order_status/<id>',views.update_order_status),
    path('update_order_status_post/<id>',views.update_order_status_post),
    path('Seller1',views.Seller1),
    path('Seller1_post',views.Seller1_post),

# ===================================================================================
    path('customer_home',views.customer_home),
    path('customer_reg',views.customer_reg),
    path('customer_reg_post',views.customer_reg_post),
    path('customer_view_profile',views.customer_view_profile),
    path('customer_view_category',views.customer_view_category),
    path('customer_view_product/<id>',views.customer_view_product),
    path('add_to_cart/<id>',views.add_to_cart),
    path('add_to_cart_post/<id>',views.add_to_cart_post),
    path('view_cart',views.view_cart),
    path('place_order/<id>',views.place_order),
    path('view_order',views.view_order),
    path('cancel_order/<id>',views.cancel_order),
    path('payment_mode/<rid>',views.payment_mode),
    path('payment_mode_post/<rid>',views.payment_mode_post),
    path('on_payment_success/<id>',views.on_payment_success),
    path('view_previous_order',views.view_previous_order),
    path('customer_send_feedback',views.customer_send_feedback),
    path('customer_send_feedback_post',views.customer_send_feedback_post),
    path('view_rating/<id>',views.view_rating),
    path('send_rating/<id>',views.send_rating),
    path('send_rating_post/<id>',views.send_rating_post),

]
