from rest_framework import serializers
from .models import *

class LogEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = LogEntry
        fields = '__all__'
    
    def to_internal_value(self, data):
        #print("data := ", data)
        metadata = data.pop("metadata")
        data["parentResourceId"] = metadata.get("parentResourceId")
        return data
        
    '''def create(self, validated_data):

        parentResourceId = validated_data.get("metadata").get("parentResourceId")

        log = LogEntry.objects.create(**validated_data)
        log.parentResourceId = parentResourceId
        log.save()
        
        return log
    '''