from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Define the Industry model
class Industry(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='industries_created')

    def __str__(self):
        return self.name

# Define the Category model
class Category(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=191)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='categories_created')

    def __str__(self):
        return self.name

# Define the Store model
class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=191)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(default='static/assets/img/logo.png', upload_to='store_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stores_created')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.logo.url
        except:
            url = ''
        return url
    
# Define the StoreLocation model
class StoreLocation(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='locations')
    address = models.TextField(blank=True, null=True, max_length=191)
    city = models.CharField(max_length=191)
    state = models.CharField(max_length=191)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=191)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='store_locations_created')

    def __str__(self):
        return f'{self.store.name} - {self.city}'

# Define the Product model
class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=191)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(default='static/assets/img/logo.png', upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True)
    digital = models.BooleanField(default=True, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products_created')

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# Define the ProductVariant model
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=191)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    additional_info = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='product_variants_created')

    def __str__(self):
        return f'{self.product.name} - {self.name}'

# Define the PaymentOption model
class PaymentOption(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payment_options_created')

    def __str__(self):
        return self.name

# Define the Customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customers_created')

    def __str__(self):
        return self.user.username

# Define the Order model
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Order {self.id} - {self.customer.user.username}'
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping 
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

# Define the OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.product_variant.name} - {self.quantity}'
    
    @property
    def get_total(self):
        total = self.product_variant.price * self.quantity
        return total
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
# Define the Payment model
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f'{self.order.id} - {self.payment_option.name}'

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.address)
    
    #trying things out
    #something cool will be build
    #setup for github
    