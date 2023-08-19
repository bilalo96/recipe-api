"""Views for the recipe APIs"""

from rest_framework import (
    viewsets,
    mixins,
    status, # to add additional functionallity
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe,Tag
from recipe import serializers

from django.shortcuts import render


# Create your views here.

class RecipeViewSet(viewsets.ModelViewSet):
    """view for manage recipe APIs"""
    serializers_class=serializers.RecipeDetailSerializer
    queryset=Recipe.objects.all()
    authentication_classes=[TokenAuthentication]
    Permission_classes=[IsAuthenticated]

    def get_queryset(self):
        """Retrive recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user.id).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializers_class

    def perform_create(self,serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

class TagViewSet(mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
               mixins.ListModelMixin,viewsets.GenericViewSet): #its important to decleare mixin before generic becauese can override some behavior
    """Manage tag in database"""
    serializer_class=serializers.TagSerializer
    queryset=Tag.objects.all()


    def get_queryset(self):
        """Filter queryset to authenticated user"""
        return self.queryset.filter(user=self.request.user.id).order_by('-name')






