from django.db import models

from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
class Booking(models.Model):
    CATEGORY_CHOICES = [
        ('1', '1 person'),
        ('2', '2 people'),
        ('3', '3 people'),
        ('4', '4 people'),
        ('family', 'Family'),
    ]
    STATUS=[
        ('1','pending'),
        ('2','declined'),
        ('3','approved'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    people = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    email = models.EmailField(max_length=100)
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='1')
class Item(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
    ]
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.DecimalField(max_digits=7,decimal_places=2)
    food=models.BooleanField(default=False,null=True,blank=False)
    offer = models.BooleanField(default=False)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    
class staff(models.Model):
    CATEGORY_CHOICES = [
        ('chef', 'Chef'),
        ('waiter', 'Waiter'),
        ('helper', 'Helper'),
        ('manager', 'Manager'),
    ]
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField(max_length=10000)
    work_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=100)
    def __str__(self):
        return self.name if self.name else "No Name"
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)
    def __str__(self):
        return str(self.id)
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product and not i.product.food:  # Check if product exists
                shipping = True
        return shipping
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total() for item in orderitems])  # Add ()
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def get_total(self):
        return self.product.price * self.quantity if self.product else 0  # Ensure product exists

# class Order(models.Model):
#     customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
#     dete_ordered=models.DateTimeField(auto_now_add=True)
#     complete=models.BooleanField(default=False,null=True,blank=False)
#     Transaction_id = models.CharField(max_length=100,null=True)
#     def __str__(self):
#         return str(self.id)
#     @property
#     def shipping(self):
#         shipping=False
#         orderitems=self.orderitem_set.all()
#         for i in orderitems:
#             if i.product.food == False:
#                 shipping = True
#         return shipping

#     @property
#     def get_cart_items(self):
#         orderitems=self.orderitem_set.all()
#         total=sum([item.quantity for item in orderitems])
#         return total
#     @property
#     def get_cart_items(self):
#         orderitems=self.orderitem_set.all()
#         total=sum([item.get_total for item in orderitems])
#         return total
# class OrderItem(models.Model):
#     product=models.ForeignKey(Item,on_delete=models.SET_NULL,blank=True,null=True)
#     order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
#     quantity = models.IntegerField(default=0,null=True,blank=True)
#     dete_added=models.DateTimeField(auto_now_add=True)
#     @property
#     def get_cart_total(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.get_total() for item in orderitems])  # Add parentheses ()
#         return total

#     def get_total(self):
#         if self.product:
#             return self.product.price * self.quantity
#         return 0
class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    pincode = models.CharField(max_length=100,null=True)
    dete_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address if self.address else "No Address"