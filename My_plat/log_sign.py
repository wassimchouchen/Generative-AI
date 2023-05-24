from django.contrib.auth import login
import jwt,datetime
from django.contrib.auth import authenticate
import requests
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import requests
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication


##authentification class for register and login(including creating user)

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        """
        Check that the username is unique.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        """
        Check that the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

@csrf_exempt  
def register(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    serializer = UserSerializer(data=body)
    if serializer.is_valid():
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        password = body.get('password') 
        user = serializer.save()        
        user.set_password(password)  
        user = serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt 
def loginn(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body.get('username')
    password = body.get('password')
    user = authenticate(request,username=username, password=password)
   
    if user:
        if user.is_active:
            login(request, user)
            secret = 'secret'
            payload = {
                'id': user.id,
                'username': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, secret , algorithm='HS256')
            response = Response()

            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
            'jwt': token}
            
            return JsonResponse({"token": token})
        else:
            return JsonResponse({"error": "User is not active."}, status=400)
    else:
        return JsonResponse({"error": "Invalid credentials."}, status=400)




class UserView(APIView):

    def get(self, request):
        token = request.headers.get('Authorization')
        print("gggg")
        
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # import pdb;pdb.set_trace()
            payload = jwt.decode(token.split()[1], 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)