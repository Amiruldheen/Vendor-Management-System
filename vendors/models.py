from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import F, Avg, Count, Case, When, ExpressionWrapper, fields

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=50)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name}"
    
    
    def calculate_on_time_delivery_rate(self):
        """
        Calculate on time delivery rating for this vendor
        """

        completed_orders_info = self.purchaseorder_set.filter(status="completed").aggregate(
            total_completed_orders=Count('id'),
            on_time_delivery_count=Count(Case(When(delivered_on__lte=F('delivery_date'), then=1)))
        )
        total_completed_orders = completed_orders_info['total_completed_orders']
        on_time_delivery_count = completed_orders_info['on_time_delivery_count']
        on_time_delivery_rate = (on_time_delivery_count/total_completed_orders)*100 if total_completed_orders > 0 else 0 
        return round(on_time_delivery_rate,2)
    

    def calculate_average_quality_rating(self):
        """
        Calculate the average quality rating for this vendor.
        """
        completed_orders = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        if completed_orders.exists():
            return completed_orders.aggregate(quality_rating_avg=Avg('quality_rating'))['quality_rating_avg']
        else:
            return None
        
    def calculate_avg_response_time(self):
        average_response_time = self.purchaseorder_set.filter(
            acknowledgement_date__isnull=False
            ).annotate(
                response_time = ExpressionWrapper(
                    (F('acknowledgement_date') - F('issue_date')),
                    output_field=fields.DurationField()
                )
            ).aggregate(
                average_response_time=Avg('response_time')
            )['average_response_time']
        return round(average_response_time.total_seconds()/3600, 2) if average_response_time else None


    def calculate_fulfillment_rate(self):
        total_orders = self.purchaseorder_set.count()
        completed_orders = self.purchaseorder_set.filter(status="completed").count()
        
        # Calculate fulfillment rate
        if total_orders > 0:
            fulfillment_rate = (completed_orders / total_orders) * 100
            return round(fulfillment_rate, 2)
        else:
            return None

    
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    delivered_on = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.CharField(max_length= 20 ,choices=STATUS_CHOICES,default='pending')
    quality_rating = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.po_number}-{self.vendor}"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"