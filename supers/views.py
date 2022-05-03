from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from super_types.models import SuperType
from .serializers import SuperSerializer
from .models import Super
from supers import serializers

@api_view(['GET'])
def supers_list(request):
    type_param = request.query_params.get('type')
    supers = Super.objects.all()
    custom_response = {}
    super_types = SuperType.objects.all()
    if type_param:
        supers = supers.filter(super_type__type=type_param)
        serializer = SuperSerializer(supers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        for super_type in super_types:
            heroes = Super.objects.filter(super_type_id=1)
            hero_serializer = SuperSerializer(heroes, many=True)
            villains = Super.objects.filter(super_type_id=2)
            villain_serializer = SuperSerializer(villains, many=True)
            custom_response = {
                "Heroes": hero_serializer.data,
                "Villains": villain_serializer.data
            }
        return Response(custom_response, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def supers_list_by_type(request):
    if request.method == 'GET':
        super_type_name = request.query_params.get('type')
        queryset = Super.objects.all()

        if super_type_name:
            queryset = queryset.filter(super_type__type=super_type_name)

        serializer = SuperSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SuperSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def super_detail(request, pk):
    super = get_object_or_404(Super, pk=pk)
    if request.method == 'GET':   
        serializer = SuperSerializer(super)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
         serializer = SuperSerializer(super, data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        super.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)