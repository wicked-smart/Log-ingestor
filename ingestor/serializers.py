from rest_framework import serializers
from .models import *

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
        