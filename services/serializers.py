
from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        # fields = '__all__'
        fields = ['id', 'name', 'image', 'description', 'price']
        read_only = ['id']
        
        
    def validate_image(self, img):
        if img is None or img =='':
            return None
        return img 
