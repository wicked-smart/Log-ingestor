from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators  import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *


# Create your views here.
@api_view(['POST'])
def ingest(request):
    if request.method == 'POST':

        data = request.data
        serializer = LogEntrySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def query(request):

    if request.method == 'POST':

        data = request.data
        try:
            message = data.pop("message")
            logs = LogEntry.objects.filter(**data, message__icontains=message)
        except LogEntry.DoesNotExists:
            return Response({"message": "No such logs exists!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LogEntrySerializer(logs, many=True,  context={"type": "query"})
        return Response(serializer.data, status=status.HTTP_200_OK)
        



