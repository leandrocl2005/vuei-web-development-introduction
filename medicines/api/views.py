from rest_framework import generics

from medicines.models import Medicine
from medicines.serializers import MedicineSerializer


class ListMedicinesAPI(generics.ListCreateAPIView):

  queryset = Medicine.objects.all()
  serializer_class = MedicineSerializer