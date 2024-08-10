from django.contrib import admin

# Register your models here.
from heyhey.models import *
admin.site.register(Industry)
admin.site.register(Category)
admin.site.register(Store)
admin.site.register(StoreLocation)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(PaymentOption)
admin.site.register(Payment)
admin.site.register(ShippingAddress)
    
