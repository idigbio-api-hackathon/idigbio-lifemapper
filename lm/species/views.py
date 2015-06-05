from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from species.models import Species
from species.serializers import SpeciesSerializer
from rest_framework import generics
from rest_framework import filters

class SpeciesList(generics.ListCreateAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('species', )


class SpeciesPrefix(generics.ListCreateAPIView):
    #queryset = Species.objects.filter(species__startswith=prefix)
    #serializer_class = SpeciesSerializer
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^species', )

class SpeciesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


#@api_view(['GET', 'POST'])
#def species_list(request):
 #   """
 #   List all species, or create a new species.
 #   """
 #   if request.method == 'GET':
 #       species = Species.objects.all()
 #       serializer = SpeciesSerializer(species, many=True)
 #       return Response(serializer.data)
#
#    elif request.method == 'POST':
#        serializer = SpeciesSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@api_view(['GET', 'PUT', 'DELETE'])
#def species_detail(request, pk):
#    """
#    Retrieve, update or delete a species instance.
#    """
#    try:
#        species = Species.objects.get(pk=pk)
#    except Species.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)
#
#    if request.method == 'GET':
#        serializer = SpeciesSerializer(species)
#        return Response(serializer.data)
#
#    elif request.method == 'PUT':
#        serializer = SpeciesSerializer(species, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    elif request.method == 'DELETE':
#        species.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
