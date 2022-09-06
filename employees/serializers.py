from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        read_only_fields = ["id"]