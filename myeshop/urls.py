"""myeshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from store import views as store_views
from account import views as account_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', store_views.home_view),
    path('home/', store_views.home_view, name='home'),
    path('search/', store_views.search_view, name='search'),
    path('register/', account_views.register_view, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('profile/', account_views.profile_view, name='profile'),
    path('editprofile/', account_views.edit_profile_view, name='editprofile'),
    path('addtocart/', store_views.add_to_cart_view, name='addtocart'),
    path('removefromcart/', store_views.remove_from_cart_view, name='removefromcart'),
    path('viewcart/', store_views.cart_view, name='viewcart'),
    path('checkout/', store_views.checkout_view, name='checkout'),
    path('placeorder/', store_views.place_order_view, name='placeorder'),
    path('vieworders/', store_views.view_orders, name='vieworders'),
    path('changepassword/', account_views.change_password_view, name='changepassword'),
    path('resetpassword/', account_views.reset_password_view, name='resetpassword'),
    path('logout/', account_views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
