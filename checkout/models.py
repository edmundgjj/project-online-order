from django.db import models

# Create your models here.

""" Model for customer details for charging purposes"""
class Charge(models.Model):
    full_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    date=models.DateField()
    
    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date, self.full_name)
        

""" Model for Transactions """
class Transaction(models.Model):
    status_options =[
        ('pending', "Pending"),
        ('approved', "Approved"),
        ('rejected', "Rejected"),
        ('uncollected', "Uncollected"),
        ('collected', "Collected")
]

    charge = models.ForeignKey('Charge', on_delete=models.CASCADE, null=True)
    status = models.CharField(blank=False, choices=status_options, max_length=50)
    date = models.DateField()
    owner = models.ForeignKey("accounts.MyUser", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return str(self.id)
        

""" Model for Line Items """
class LineItem(models.Model):
    product = models.ForeignKey('menu.Menu', on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    cost = models.IntegerField(blank=False)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name + " : " + self.sku