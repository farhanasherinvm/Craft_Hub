from django.urls import path
from .views import Reviewcreateview,Reviewlist,Replyreview


urlpatterns = [
    path('reviewcreate/',Reviewcreateview.as_view(),name='review-create'),
    path('product/<int:product_id>/reviewlist/',Reviewlist.as_view(),name='review-list'),
    path('replyreview/<int:pk>/',Replyreview.as_view(),name='reply-review')
]