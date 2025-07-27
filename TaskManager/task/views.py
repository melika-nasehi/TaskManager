from django.core.serializers import serialize
from django.http import HttpResponse, Http404
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_203_NON_AUTHORITATIVE_INFORMATION, HTTP_200_OK
from rest_framework.views import APIView
from .serialize import *
from rest_framework import status
from .models import Task



# Create your views here.

class TaskList(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        serialized_task = TaskSerializer(tasks, many=True)
        return Response(serialized_task.data)

    def post(self, request):
        serialized_task = TaskSerializer(data=request.data)
        if serialized_task.is_valid():
            serialized_task.save()
            return Response(serialized_task.data, status=status.HTTP_201_CREATED)
        return Response(serialized_task.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetails(APIView):
    def get_object(self, pk):
        try :
            return Task.objects.get(pk= pk)
        except :
            raise Http404


    def get(self, request, pk):
        task = self.get_object(pk = pk)
        serialized_task = TaskSerializer(task)
        return Response(serialized_task.data)

    def put(self, request, pk):
        task = self.get_object(pk = pk)
        serialized_task = TaskSerializer(task, data=request.data, partial=True)
        if serialized_task.is_valid():
            serialized_task.save()
            return Response(serialized_task.data, status=status.HTTP_201_CREATED)
        return Response(serialized_task.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        task = self.get_object(pk=pk)
        title = task.title
        task.delete()
        return Response("{} deleted successfully !".format(title), status=HTTP_200_OK)


class ToggleCompleted (APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        user = request.user

        try:
            task = Task.objects.get(id=task_id, users__in=[user])
        except Task.DoesNotExist:
            return Response("not found")

        task.is_completed = not task.is_completed
        task.save()
        return Response("is_completed: " + str(task.is_completed))

