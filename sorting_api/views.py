from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class BubbleSortView(APIView):
    def post(self, request):
        # read array from request.data
        # run sorting logic
        # return JSON
        return Response(...)