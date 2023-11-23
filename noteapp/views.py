from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . serializers import UserRegistrationSerializer,UserLoginSerializer,NoteSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework import generics
from .models import User,Note
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    def post(self,requset,format=None):
        serilizer = UserRegistrationSerializer(data=requset.data)
        if serilizer.is_valid(raise_exception=True):
            user=serilizer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    def post(self,request,format=None):
        serilizer = UserLoginSerializer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            email=serilizer.data.get('email')
            password=serilizer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_fields_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response({'msg':'Login Success'},status=status.HTTP_400_BAD_REQUEST)
    
    
class CreateNoteView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer



class NoteView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'updated_at']
    search_fields = ['title', 'content']

    def get(self, request, *args, **kwargs):
        notes = Note.objects.all()
        paginated_notes = self.paginate_queryset(notes)
        serializer = NoteSerializer(paginated_notes, many=True)
        return self.get_paginated_response(serializer.data)


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                pass
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
