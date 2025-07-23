from django.db import models
from django.utils import timezone
from product.models import Product
from users.models import CustomUser

    
class Cartitem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class Wishlist(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,)
    wishlistitems=models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.wishlistitems} added to wishlist"