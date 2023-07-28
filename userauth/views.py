from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
# Create your views here.

# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def example_view(request, format=None):
#     content = {
#         'user': str(request.user),  # `django.contrib.auth.User` instance.
#         'auth': str(request.auth),  # None
#     }
#     return Response(content)

@csrf_exempt
def auth(request, format=None):
    if request.method=='POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        # return JsonResponse("Added Succesfully!!", safe=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse("Added Succesfully!!", safe=False)
        return JsonResponse("Invalid Format", safe=False)