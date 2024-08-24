from django.db import models
import os
from django.contrib.auth.models import User

class Key(models.Model):
    key = models.CharField(max_length=30)

    def __str__(self):
        return self.key

class Good(models.Model):

    categoty_choices = [('br', 'Bedroom'), 
                        ('dn', 'Dining'), 
                        ('of', 'Office'), 
                        ('lr', 'Livingroom')]

    name = models.CharField(max_length=30, unique=True)
    category = models.CharField(max_length=2, choices=categoty_choices)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField()
    img = models.ImageField(upload_to='images/')
    stock = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    depth = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    materials = models.CharField(max_length=70)
    style = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    accessories = models.CharField(max_length=70)

    def __str__(self):
        return f'{self.name}, {self.price}, {self.category}, {self.stock}'
    
    def delete(self, *args, **kwargs):
        if self.img:
            img_path = self.img.path
            
            if os.path.isfile(img_path):
                os.remove(img_path)
                print(f'Successfully deleted image at: {img_path}')

        
        super().delete(*args, **kwargs)
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def update_total_price(self):
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_price = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Good, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.price

