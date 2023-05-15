from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.conf import settings
from decimal import Decimal

class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstName

    
    
class Car(models.Model):
    id_car = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    license = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    version = models.CharField(max_length=100, blank=True)
    serieNumber = models.CharField(max_length=100, blank=True)
    vin = models.CharField(max_length=100, blank=True)
    engine = models.CharField(max_length=100, blank=True)
    oil = models.CharField(max_length=100, blank=True)
    traction = models.CharField(max_length=100, blank=True)
    comments = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='image/', null=True, blank=True)

    def __str__(self):
        return self.brand + ' ' + self.model + ' ' + self.year

        

class Services(models.Model):
    id_service = models.AutoField(primary_key=True)
    id_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)    
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    mechanic = models.CharField(max_length=100)
    comments = models.CharField(max_length=250)
    cost = models.DecimalField(max_digits=6, decimal_places=2)    
    total_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    SERVICE_CHOICES=[
        ('TYRES', 'Tyres'),
        ('SUSPENSION', 'Suspension'),
        ('BREAKS', 'Breaks'),
        ('OIL', 'Oil'),
        ('PAINT', 'Paint'),
        ('BODYWORK', 'Bodywork'),
        ('ENGINE', 'Engine'),
        ('FAN', 'Fan'),
        ('ELECTRIC', 'Electric'),
        ('SCANNER', 'Scanner'),
        ('WASH', 'Wash'),
        ('GENERAL_INSPECTION', 'General Inspection'),
        ('MUFFLE', 'Muffle'),
        ('OTHER', 'Other')
    ]
    
    services = MultiSelectField(choices=SERVICE_CHOICES, verbose_name='Services provided')
    
    def __str__(self):
        return self.description
    
    def GST_cost(self):
        subtotal = self.cost
        GST_cost = subtotal * Decimal(settings.TAX_GST)
        return GST_cost.quantize(Decimal('0.01'))
    
    def QST_cost(self):
        subtotal = self.cost
        QST_cost = subtotal * Decimal(settings.TAX_QST)
        return QST_cost.quantize(Decimal('0.01'))
        
    
    def total_cost(self):
        subtotal = self.cost        
        total_cost = subtotal + self.GST_cost() + self.QST_cost()
        return total_cost

