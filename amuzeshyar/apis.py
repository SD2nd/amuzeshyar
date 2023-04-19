from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import (
    PersonSerializer,
    EmailSerializer,
    PhoneNumberSerializer,
    StudentResponseSerializer, 
    StudentRequestSerializer, 
    AddressSerializer)
from .models import Person as PersonModel
from .models import Student as StudentModel



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
    
class Student(APIView):
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id', None)
        if student_id: 
            student = StudentModel.objects.filter(id=student_id).first()
            if student: 
                serialized_data = StudentResponseSerializer(instance=student).data
                return Response(
                    {
                    "msg":"success",
                    "data":serialized_data
                    },
                    status=status.HTTP_200_OK
                    )
            return Response({"msg":"student not found"},status=status.HTTP_404_NOT_FOUND)
        return Response({"msg":"student id is required"},status=status.HTTP_400_BAD_REQUEST)
            

    
    def post(self, request, *args, **kwargs):
        payload = request.data
        national_id = payload.get('national_id')
        if payload and national_id:
            emails = request.data.get('emails', [])
            phone_numbers = request.data.get('phone_numbers',[])
            addresses = request.data.get('addresses',[])
            
            # making emails, phone numbers, addresses objects
            emails_data = [{"email": email, "person":national_id} for email in emails]
            phone_numbers_data = [{"number": phone, "person": national_id} for phone in phone_numbers]
            addresses_data = [{"address": address, "person": national_id} for address in addresses]
            
            person_ser = PersonSerializer(data=payload)
            student_ser = StudentRequestSerializer(data=payload)
            email_ser = EmailSerializer(data=emails_data, many=True)
            phone_number_ser = PhoneNumberSerializer(data=phone_numbers_data, many=True)
            address_ser = AddressSerializer(data=addresses_data, many=True)
            
            is_all_valid = all([
                person_ser.is_valid(),
                student_ser.is_valid(),
                phone_number_ser.is_valid(),
                address_ser.is_valid(),
                email_ser.is_valid()
            ])
            if is_all_valid:
                person_ser.save()
                student_ser.save()
                phone_number_ser.save()
                address_ser.save()
                email_ser.save()
                
                # preparing student data for response display
                student = StudentModel.objects.filter(student_id=student_ser.student_id).first()
                student_data = StudentResponseSerializer(student).data
                return Response(
                    {
                    "msg":"success",
                    "data": student_data
                    },
                    status=status.HTTP_201_CREATED
                )
            else: 
                all_errors = []
                if person_ser.errors: all_errors.append(person_ser.errors)
                if student_ser.errors: all_errors.append(student_ser.errors)
                if phone_number_ser.errors: all_errors.append(phone_number_ser.errors)
                if address_ser.errors: all_errors.append(address_ser.errors)
                if email_ser.errors: all_errors.append(email_ser.errors)
                return Response(
                    {
                    "msg":"failure",
                    "detail": all_errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                      
        return Response(
            {
            "msg":"failure",
            "detail": "payload is required"
            },
            status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        pass
    
    def patch(self, request, *args, **kwargs):
        pass
    
    def delete(self, request, *args, **kwargs):
        pass
    
    @api_view(['GET'])
    def get_students(request, *args, **kwargs):
        pass