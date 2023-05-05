from django.urls import path
from . import views

urlpatterns = [
    path('signin',views.signin,name='signin'),
    path('logout',views.logout,name='logout'),
    path('signup',views.signup,name='signup'),
    path('profile',views.profile,name='profile'),
    path('product_favorite/<int:pro_id>',views.favorite_pro,name='fav_pro'),
    path('favorite_products',views.favorite_products,name='favorite_products')
]
