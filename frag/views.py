from .models import Frags
from .serializers import FragSerializer, TitleSerializer
from django.shortcuts import render
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_data(request, format=None):
    request_data = JSONParser().parse(request)
    abstract = request_data.get('abstract')
    title = request_data.get('title')
    data = request_data.get('data')
    # print(request.user)
    my_model = Frags(abstract=abstract, user=request.user,
                     title=title, data=data)
    my_model.save()
    return JsonResponse("Added Succesfully!!", safe=False)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_data(request, format=None):
    request_data = JSONParser().parse(request)
    title = request_data.get('title')
    obj = Frags.objects.filter(user=request.user, title=title)
    obj.delete()
    return JsonResponse("Deleted Succesfully!!", safe=False)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request, format=None):
    request_data = JSONParser().parse(request)
    title = request_data.get('title')
    my_model = Frags.objects.filter(user=request.user, title=title)
    serialized = FragSerializer(my_model, many=True)
    return JsonResponse(serialized.data, safe=False)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_title(request):
    titles = Frags.objects.filter(user=request.user).values('title')
    print(titles)
    serialized = TitleSerializer(titles, many=True)
    return JsonResponse(serialized.data, safe=False)
