from django.db import models

# Create your models here.

class login(models.Model):
    Username=models.CharField(max_length=255)
    Password=models.CharField(max_length=255)
    Usertype=models.CharField(max_length=100)

class seller(models.Model):
    Name=models.CharField(max_length=255)
    Email=models.EmailField(max_length=255)
    Phone=models.CharField(max_length=255)
    Place=models.CharField(max_length=255)
    Post=models.CharField(max_length=255)
    PIN=models.BigIntegerField()
    LOGIN=models.ForeignKey(login,on_delete=models.CASCADE)

class customer(models.Model):
    Name=models.CharField(max_length=255)
    Email=models.EmailField(max_length=255)
    Phone=models.CharField(max_length=255)
    Place=models.CharField(max_length=255)
    Post=models.CharField(max_length=255)
    PIN=models.BigIntegerField()
    LOGIN=models.ForeignKey(login,on_delete=models.CASCADE)

class category(models.Model):
    Name=models.CharField(max_length=255)

class feedback(models.Model):
    Feedback=models.CharField(max_length=255)
    Date=models.CharField(max_length=100)
    CUSTOMER=models.ForeignKey(customer,on_delete=models.CASCADE)

class product(models.Model):
    Name=models.CharField(max_length=255)
    Price=models.CharField(max_length=255)
    Image=models.CharField(max_length=255)
    Description=models.CharField(max_length=255)
    SELLER=models.ForeignKey(seller,on_delete=models.CASCADE,default=1)
    CATEGORY = models.ForeignKey(category, on_delete=models.CASCADE,default=1)


class cart(models.Model):
    PRODUCT=models.ForeignKey(product,on_delete=models.CASCADE)
    CUSTOMER=models.ForeignKey(customer,on_delete=models.CASCADE)
    Quantity=models.CharField(max_length=100)

class orderr(models.Model):
    CUSTOMER=models.ForeignKey(customer,on_delete=models.CASCADE)
    PRODUCT=models.ForeignKey(product,on_delete=models.CASCADE)
    Amount=models.CharField(max_length=100)
    Date=models.DateField()
    Payment_Status=models.CharField(max_length=255)
    Payment_Date=models.CharField(max_length=255)
    Status=models.CharField(max_length=255)

class ordersub(models.Model):
    ORDERR=models.ForeignKey(orderr,on_delete=models.CASCADE)
    Quantity=models.CharField(max_length=255)
    order_date=models.CharField(max_length=255)

class Rating(models.Model):
    CUSTOMER = models.ForeignKey(customer, on_delete=models.CASCADE)
    PRODUCT = models.ForeignKey(product, on_delete=models.CASCADE)
    Rating= models.CharField(max_length=100)
    date = models.CharField(max_length=100)