from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.response import Response

class EmployeeViewset(viewsets.ModelViewSet):
  queryset = models.Employee.objects.all()
  serializer_class = serializers.EmployeeSerializer
  def delete(self, request, *args, **kwargs):
    models.Employee.objects.all().delete()
    return Response("hello")