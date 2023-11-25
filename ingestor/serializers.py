from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
import re

class LogEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = LogEntry
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        type = self.context.get("type")
        if type is not None and type == 'query':
            for field_name in self.fields.keys():
                self.fields[field_name].allow_null = True
                self.fields[field_name].required = False


    def to_internal_value(self, data):
        #print("data := ", data)
        metadata = data.pop("metadata")
        data["parentResourceId"] = metadata.get("parentResourceId")
        return data
        

class LogQueryParamsSerializer(serializers.ModelSerializer):

    from_timestamp = serializers.CharField(required=False, max_length=100)
    to_timestamp = serializers.CharField(required=False, max_length=100)

    class Meta:
        model = LogEntry
        fields = ["level", "message", "resourceId", "timestamp", "traceId", "spanId", "commit", "parentResourceId", "from_timestamp", "to_timestamp"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].allow_null=True
            self.fields[field_name].required=False

    
    def validate(self, attrs):

        timestamp = attrs.get("timestamp")

        from_timestamp= attrs.get("from_timestamp")
        to_timestamp = attrs.get("to_timestamp")

        if (from_timestamp and (to_timestamp is None)) or (to_timestamp and (from_timestamp is None)):
            raise ValidationError("from_timestamp and to_timestamp is both neccessary!")

        if timestamp and (from_timestamp and to_timestamp):
            raise ValidationError("timestamp field cannot be as a filter with timestamp range (from and to)!")

        #validate from and to timestamp's format
        if from_timestamp and to_timestamp:
            pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
            print(type(from_timestamp))
            match1 = pattern.fullmatch(from_timestamp)
            match2 = pattern.fullmatch(to_timestamp)

            if match1 is None or match2 is None:
                raise ValidationError("Timestamp must be int UTC format YYYY-mm-ddTHH:MM:SSZ")


        return attrs