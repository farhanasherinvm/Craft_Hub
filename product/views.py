from rest_framework import generics, status,permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .models import Product, ProductImage,ProductCategory
from .serializers import ProductSerializer,ProductImageSerializer,ProductCategorySerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated] 

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED)


class ProductListRetrieveView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'product_code', 'description']
    filterset_fields = ['product_type', 'size']  # Add more fields if needed
    ordering_fields = ['price', 'created_at', 'updated_at']


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated] 
    lookup_field = 'id'


class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated] 
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
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product_name = product.name
        self.perform_destroy(product)
        return Response({"message": f"Product '{product_name}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class ProductImageUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView):
    def get(self, request, id):
        category = get_object_or_404(ProductCategory, id=id)
        serializer = ProductCategorySerializer(category)
        return Response(serializer.data)


class CategoryUpdateView(APIView):
    def put(self, request, id):
        category = get_object_or_404(ProductCategory, id=id)
        serializer = ProductCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    def delete(self, request, id):
        category = get_object_or_404(ProductCategory, id=id)
        category_name = category.name
        category.delete()
        return Response({"message": f"Category '{category_name}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)