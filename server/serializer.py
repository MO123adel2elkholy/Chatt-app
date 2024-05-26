from .models import (Category, Server, Chnnel)
from rest_framework import serializers


class CategorySeralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ChnnelSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Chnnel
        fields = '__all__'


class ServerSeralizer(serializers.ModelSerializer):
    channels = ChnnelSeralizer(many=True)
    subscriper = serializers.SerializerMethodField()

    class Meta:
        model = Server
        exclude = ("members",)

    def get_subscriper(self, obj):
        if hasattr(obj, 'subscriper'):
            return obj.subscriper
        return None
    #  this methode for returning data if it required or not

    def to_representation(self, instance):

        data = super().to_representation(instance)
        subscriper = self.context.get('subscriper')
        if not subscriper:
            data.pop(' ', None)
            return data
