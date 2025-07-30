from rest_framework import generics, status,permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .models import Product, ProductImage,ProductCategory
from .serializers import ProductSerializer,ProductImageSerializer,ProductCategorySerializer
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Cart, CartItem, Wishlist
from .serializers import CartSerializer, CartItemSerializer, WishlistSerializer
from rest_framework.decorators import action




class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser] 

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)


class ProductListRetrieveView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ['price', 'created_at', 'updated_at']


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [AllowAny] 
    lookup_field = 'id'


class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser] 
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Handle new image uploads
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return Response(self.get_serializer(product).data, status=status.HTTP_200_OK)

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product_name = product.name
        self.perform_destroy(product)
        return Response({"message": f"Product '{product_name}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class ProductImageUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, id):
        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        images = request.FILES.getlist('images')
        if not images:
            return Response({'error': 'No images provided'}, status=status.HTTP_400_BAD_REQUEST)

        image_objs = []
        for img in images:
            image_obj = ProductImage.objects.create(product=product, image=img)
            image_objs.append(image_obj)

        serializer = ProductImageSerializer(image_objs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class CategoryCreateView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView):
    permission_classes=[AllowAny]
    def get(self, request, id):
        category = get_object_or_404(ProductCategory, id=id)
        serializer = ProductCategorySerializer(category)
        return Response(serializer.data)


class CategoryUpdateView(APIView):
    permission_classes=[IsAdminUser]
    def put(self, request, id):
        category = get_object_or_404(ProductCategory, id=id)
        serializer = ProductCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    permission_classes=[IsAdminUser]
    def delete(self, request, id):
        category = get_object_or_404(ProductCategory, id=id)
        category_name = category.name
        category.delete()
        return Response({"message": f"Category '{category_name}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name','product_code','stock_keeping_unit','description', 'color']


class ProductFilterView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category','product_type','fabric','allow_customization', 'is_draft']




class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, saved_for_later=False)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, saved_for_later=False)
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            total_quantity = quantity if created else cart_item.quantity + quantity

            if total_quantity > product.current_stock:
                return Response(
                    {"error": f"Only {product.current_stock} items left in stock for {product.name}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = total_quantity
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            quantity = serializer.validated_data.get('quantity', cart_item.quantity)

            if quantity > cart_item.product.current_stock:
                return Response(
                    {"error": f"Only {cart_item.product.current_stock} items available for {cart_item.product.name}"},
                    status=400
                )

            cart_item.quantity = quantity
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='save-for-later')
    def save_for_later(self, request):
        cart_item_id = request.data.get("cart_item_id")
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)

        saved_cart, _ = Cart.objects.get_or_create(user=request.user, saved_for_later=True)
        # Move item to saved cart
        cart_item.cart = saved_cart
        cart_item.save()

        return Response({"message": "Item moved to saved for later."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='saved-items')
    def view_saved_items(self, request):
        saved_cart = Cart.objects.filter(user=request.user, saved_for_later=True).first()
        if not saved_cart:
            return Response({"message": "No saved items."}, status=status.HTTP_204_NO_CONTENT)
        serializer = CartSerializer(saved_cart)
        return Response(serializer.data)

   
class WishlistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        wishlist_item = self.get_object()
        wishlist_item.delete()
        return Response({"message": "Item removed from wishlist."}, status=status.HTTP_204_NO_CONTENT)
