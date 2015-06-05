from django.forms import widgets
from rest_framework import serializers
from species.models import Species


class SpeciesSerializer(serializers.Serializer):
    species = serializers.CharField(required=True, allow_blank=False, max_length=100)
    specimens = serializers.IntegerField(required=True, min_value=0)

    def create(self, validated_data):
        """
        Create and return a new `Species` instance, given the validated data.
        """
        return Species.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Species` instance, given the validated data.
        """
        instance.species = validated_data.get('species', instance.species)
        instance.specimens = validated_data.get('specimens', instance.species)
        instance.save()
        return instance
