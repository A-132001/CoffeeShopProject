from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from creditcards.models import CardNumberField,CardExpiryField,SecurityCodeField

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    details = models.ManyToManyField(Product,through='OrderDetails')
    is_finished = models.BooleanField()
    total = 0
    count = 0
    def __str__(self):
        return 'User: '+ self.user.username +', Order id'+ str(self.id)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    quantity = models.IntegerField()
    
    def __str__(self): 
        return 'User: ' + self.order.user.username + ', Product: ' +self.product.name+', Order id: '+ self.order.id
    
    class Meta:
      ordering = ['id']
      
      
      
class Payment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    card_number = CardNumberField()
    expire = CardExpiryField(default=None)
    security_code = SecurityCodeField(default=None)
    