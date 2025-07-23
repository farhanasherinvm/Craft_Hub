from django.urls import path
from .views import (
                Cartcreateview,
                Cartupdateview,
                CartListview,
                Cartdeleteview,
                Wishlistview,
                Wishlistdeleteview
)

urlpatterns = [
    path('cartlist/',CartListview.as_view(), name='cart-list'),
    path('cartadd/', Cartcreateview.as_view(), name='cart-add'),
    path('update/<int:pk>/', Cartupdateview.as_view(), name='cart-update'),
    path('delete/<int:pk>/', Cartdeleteview.as_view(), name='cart-delete'),
    path('wishlist/',Wishlistview.as_view(),name='wish-listview'),
    path('createwishlist/',Wishlistview.as_view(),name='create-wishlist'),
    path('deletewishlist/<int:pk>/',Wishlistdeleteview.as_view(),name='Wishlist-delete')
]