"""
Model Serializers
"""
from rest_framework.serializers import ModelSerializer

from .models import Customer


class CustomerAvatarSerializer (ModelSerializer):
    """
    Serialize Customer Avatar Data
    """

    class Meta:
        model = Customer
        fields = ['avatar']
    #
    # def save (self, *args, **kwargs):
    #     if self.instance.avatar:
    #         self.instance.avatar.delete()
    #     return super().save(*args, **kwargs)
