from django.urls import path
from .views import (
    ProductCreateView,
    ProductListRetrieveView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,ProductImageUploadView, CategoryCreateView,
    CategoryListView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/', ProductListRetrieveView.as_view(), name='product-list-search'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:id>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:id>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/<int:id>/upload_images/', ProductImageUploadView.as_view(), name='product-upload-images'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:id>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:id>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
]
