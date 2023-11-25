from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators  import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from datetime import date, datetime


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
        queryParamSerializer = LogQueryParamsSerializer(data=data)
        if queryParamSerializer.is_valid():
            try:
                message = queryParamSerializer.validated_data.pop("message")
                
                 
                from_timestamp = queryParamSerializer.validated_data.get("from_timestamp")
                to_timestamp = queryParamSerializer.validated_data.get("to_timestamp")

                if from_timestamp and to_timestamp:
                    from_timestamp_val = queryParamSerializer.validated_data.pop("from_timestamp")
                    to_timestamp_val = queryParamSerializer.validated_data.pop("to_timestamp")


                # get the regex'ed query first then filter remaining on top of it
                raw_message = rf"{message}"
                logs = LogEntry.objects.filter(message__regex=raw_message)
                logs = logs.filter(**queryParamSerializer.validated_data)
        
                
                if from_timestamp and to_timestamp:
                    from_timestamp = datetime.strptime(from_timestamp_val, "%Y-%m-%dT%H:%M:%SZ")
                    to_timestamp = datetime.strptime(to_timestamp_val, "%Y-%m-%dT%H:%M:%SZ")
                    logs = logs.filter(timestamp__gte=from_timestamp, timestamp__lte=to_timestamp)
                


                ## ADD PAGINATION and ROLE BASED / meaning permission class appropriate
                serializer = LogEntrySerializer(logs, many=True,  context={"type": "query"})
                return Response(serializer.data, status=status.HTTP_200_OK)

            except LogEntry.DoesNotExists:
                return Response({"message": "No such logs exists!"}, status=status.HTTP_200_OK)

        else:
            return Response(queryParamSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        



