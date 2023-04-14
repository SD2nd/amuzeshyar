from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import PersonSerializer


# create your api here
# https://www.django-rest-framework.org/tutorial/quickstart/

class Person(APIView):    
    def post(self, request):
        data = request.data
        if data: 
            serialized = PersonSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status.HTTP_201_CREATED)
            return Response({"erorr":"data is unvalid",'details':serialized.errors}, status.HTTP_400_BAD_REQUEST )
        return Response({"erorr":"empty payload"},status.HTTP_400_BAD_REQUEST )
              