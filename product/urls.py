from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet,WishlistViewSet
from .views import (
    ProductCreateView,
    ProductListRetrieveView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,ProductImageUploadView, CategoryCreateView,
    CategoryListView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,ProductSearchView,ProductFilterView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

# # Manual mapping for CartViewSet .
cart_list = CartViewSet.as_view({
    'get': 'list',     # View cart
    'post': 'create',  # Add to cart
})

cart_detail = CartViewSet.as_view({
    'put': 'update',    # Update quantity
    'patch': 'update',  # Update quantity (partial)
    'delete': 'destroy' # Remove from cart
})



urlpatterns = [
    # Product CRUD
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/', ProductListRetrieveView.as_view(), name='product-list'),  # ?page=1
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:id>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:id>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Product Search and Filter
    path('products/search/', ProductSearchView.as_view(), name='product-search'),  # ?search=laptop
    path('products/filter/', ProductFilterView.as_view(), name='product-filter'),  # ?product_type=Shirt&size=Large&page=1

    # Product Image Upload
    path('products/<int:id>/upload_images/', ProductImageUploadView.as_view(), name='product-upload-images'),

    # Category CRUD
    path('categories/', CategoryListView.as_view(), name='category-list'),  # ?page=1
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:id>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:id>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    # Auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', cart_list, name='cart'),               # GET, POST
    # path('cart/<int:pk>/', cart_detail, name='cart-detail'),  # PUT, PATCH, DELETE
    path('', include(router.urls)),                      # wishlist/

    # Add custom cart action endpoints
    path('cart/save-for-later/', CartViewSet.as_view({'post': 'save_for_later'}), name='cart-save-for-later'),
    path('cart/saved-items/', CartViewSet.as_view({'get': 'view_saved_items'}), name='cart-saved-items'),
    
]