from django.shortcuts import render
from django.db.models import F, Count, Case, When

from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, PurchaseOrderAcknowledgeSerializer, HistoricalPerformanceSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated


from time import timezone
from datetime import date
# Create your views here.
@api_view(['GET'])
def home(request):
    return Response("Vendor Management System")

@permission_classes([IsAuthenticated])
class CreateVendor(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def perform_create(self, serializer):
        last_vendor = Vendor.objects.all().order_by('id').last()
        if not last_vendor:
            vendor_code = 'VENDOR0001'
        else:
            last_code = last_vendor.vendor_code
            code_number = int(last_code.split('VENDOR')[-1]) + 1
            vendor_code = 'VENDOR{:04d}'.format(code_number)
        serializer.save(vendor_code=vendor_code)

        # instance = serializer.instance
        # instance.on_time_delivery_rate = instance.calculate_on_time_delivery_rate()
        # instance.quality_rating_avg = instance.calculate_average_quality_rating()
        # instance.average_response_time = instance.calculate_avg_response_time()
        # instance.fulfillment_rate = instance.calculate_fulfillment_rate()
        # instance.save()



    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = []
        for instance in queryset:
            
            on_time_delivery_rate = instance.calculate_on_time_delivery_rate()
            quality_rating_avg = instance.calculate_average_quality_rating()
            average_response_time = instance.calculate_avg_response_time()
            fulfillment_rate = instance.calculate_fulfillment_rate()

            # Serialize the vendor data
            serializer = self.get_serializer(instance)
            serialized_data = serializer.data

            serialized_data['on_time_delivery_rate'] = on_time_delivery_rate
            serialized_data['quality_rating_avg'] = quality_rating_avg
            serialized_data['average_response_time'] = average_response_time
            serialized_data['fulfillment_rate'] = fulfillment_rate

            data.append(serialized_data)
        return Response(data)
    
@permission_classes([IsAuthenticated])
class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        on_time_delivery_rate = instance.calculate_on_time_delivery_rate()
        quality_rating_avg = instance.calculate_average_quality_rating()
        average_response_time = instance.calculate_avg_response_time()
        fulfillment_rate = instance.calculate_fulfillment_rate()

        serializer = self.get_serializer(instance)
        data = serializer.data
        data['on_time_delivery_rate'] = on_time_delivery_rate
        data['quality_rating_avg'] = quality_rating_avg
        data['average_response_time'] = average_response_time
        data['fulfillment_rate'] = fulfillment_rate


        return Response(data)

@permission_classes([IsAuthenticated])
class CreatePurchaseOrder(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def perform_create(self, serializer):
        last_purchase_order = PurchaseOrder.objects.all().order_by('id').last()
        if not last_purchase_order:
            po_number = 'PO_0001'
        else:
            last_code = last_purchase_order.po_number
            code_number = int(last_code.split('PO_')[-1]) + 1
            po_number = 'PO_{:04d}'.format(code_number)
        serializer.save(po_number=po_number)

@permission_classes([IsAuthenticated])
class PurchaseOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

@permission_classes([IsAuthenticated])
class PurchaseOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


# Performance Metrics
@permission_classes([IsAuthenticated])
class VendorPerformance(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        on_time_delivery_rate = instance.calculate_on_time_delivery_rate()
        quality_rating_avg = instance.calculate_average_quality_rating()
        average_response_time = instance.calculate_avg_response_time()
        fulfillment_rate = instance.calculate_fulfillment_rate()

        # Update metrics in the vendor instance
        instance.on_time_delivery_rate = on_time_delivery_rate
        instance.quality_rating_avg = quality_rating_avg
        instance.average_response_time = average_response_time
        instance.fulfillment_rate = fulfillment_rate
        instance.save()

        serializer = self.get_serializer(instance)
        data = serializer.data
        # data['on_time_delivery_rate'] = on_time_delivery_rate
        # data['quality_rating_avg'] = quality_rating_avg
        # data['average_response_time'] = average_response_time
        # data['fulfillment_rate'] = fulfillment_rate
        

        return Response(data)
    
@permission_classes([IsAuthenticated])
class AcknowledgePurchaseOrder(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderAcknowledgeSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the PurchaseOrder instance
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class HistoricalPerformanceCreateView(generics.CreateAPIView):
    serializer_class = HistoricalPerformanceSerializer

    def perform_create(self, serializer):
        # Fetch the vendor for which historical performance is being logged
        vendor = Vendor.objects.get(id=self.kwargs['pk'])
        
        # Fetch performance metrics from the vendor model
        on_time_delivery_rate = vendor.calculate_on_time_delivery_rate()
        quality_rating_avg = vendor.calculate_average_quality_rating()
        average_response_time = vendor.calculate_avg_response_time()
        fulfillment_rate = vendor.calculate_fulfillment_rate()
        
        # Create the historical performance record
        serializer.save(
            vendor=vendor,
            on_time_delivery_rate=on_time_delivery_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate
        )