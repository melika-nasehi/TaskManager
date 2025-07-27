
from django.shortcuts import render
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from task.models import Task
from task.serialize import TaskSerializer
from datetime import date
from project.models import Project
from project.serializer import ProjectSerializer


# Create your views here.

class UserList (APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serialized_user = UserSerializer(users, many=True)
        return Response(serialized_user.data)

    def post(self, request):
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)

        return Response(serialized_user.errors, status=HTTP_400_BAD_REQUEST)


class UserDetail (APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk= pk)
        except :
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk= pk)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)


    def put(self, request, pk):
        user = self.get_object(pk)
        serialized_user = UserSerializer(user, data = request.data, partial=True)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data)

        return Response(serialized_user.errors, status= status.HTTP_400_BAD_REQUEST)


    def delete (self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(f"{user.username} deleted successfully" , status=status.HTTP_204_NO_CONTENT)



    class LoginView(APIView):
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        permission_classes = [IsAuthenticated]

        def get(self, request, format=None):
            content = {
                'user': str(request.user),
                'auth': str(request.auth),
            }
            return Response(content)


class GetNOTCompletedTasks (APIView):
    def get(self, request, user_id):
        tasks = Task.objects.filter(users__id=user_id, is_completed=False)
        serialized_task = TaskSerializer(tasks, many=True)
        return Response(serialized_task.data)


class DeadlineExpired (APIView):
    def get(self, request, user_id):
        now = date.today()
        task = Task.objects.filter(users__id=user_id, deadline__lt=now)
        serialize = TaskSerializer(task, many=True)
        return Response(serialize.data)


class SortProjectByStartDate (APIView):
    def get(self, request, user_id):
        projects = Project.objects.filter(users__id=user_id).order_by('startDate')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)




