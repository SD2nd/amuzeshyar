from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import PersonSerializer,EmailSerializer, PhoneNumberSerializer
from .models import Person as PersonModel


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

    def get(self, request, national_id):
        queryset = PersonModel.objects.get(national_id =national_id )
        serialized = PersonSerializer(queryset, many=True)
        return Response(serialized.data, status.HTTP_200_OK)

    def delete(self, request, national_id):
        qs = PersonModel.objects.filter(national_id = national_id).first()
        if qs: 
            qs.delete()
            return Response({"msg":"deleted"}, status.HTTP_200_OK)
        return Response({"msg":"not found"},status.HTTP_404_NOT_FOUND)


# @api_view(['DELETE'])
# def del_person(self, request, national_id):
#     qs = PersonModel.objects.filter(national_id = national_id).first()
#     if qs: 
#         serialized = PersonSerializer(instance=qs)
#         return Response(serialized.data, status.HTTP_200_OK)
#     return Response({"msg":"not found"},status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def register_student(request):
    
    email_address = request.data.get('email')
    phone_number = request.data.get('phone_number')
    person_data = request.data
    
    serialized = PersonSerializer(data=person_data)
    if serialized.is_valid():
        serialized.save()
        person_id = serialized.data.get("national_id")

    # handling email 
    email_data = {
        "email": email_address,
        "person": person_id
    }
    
    email_serialized = EmailSerializer(data=email_data)
    if email_serialized.is_valid():
        email_serialized.save()
    
    # handling phonenumber 
    phone_data = {
        "number": phone_number,
        "person": person_id
    }
    
    phone_serialized = PhoneNumberSerializer(data=phone_data)
    if phone_serialized.is_valid():
        phone_serialized.save()
    
    return Response({"msg": "Success"}, status=status.HTTP_201_CREATED)
    
    