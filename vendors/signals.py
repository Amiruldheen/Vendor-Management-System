from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, created, **kwargs):

    if instance.pk: 
        try:
            old_instance = PurchaseOrder.objects.get(pk=instance.pk) 
        except PurchaseOrder.DoesNotExist:
            return  

        if instance.status != old_instance.status:
            # Call the calculate_metrics method of the vendor associated with the purchase order
            
            instance.vendor.calculate_on_time_delivery_rate()
            instance.vendor.calculate_average_quality_rating()
            instance.vendor.calculate_avg_response_time()
            instance.vendor.calculate_fulfillment_rate()
