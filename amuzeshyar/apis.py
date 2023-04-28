from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from amuzeshyar import (
    serializers as s,
    models as m
)


class Person(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        if data:
            serialized = s.PersonRequestSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status.HTTP_201_CREATED)
            return Response({"error": "data is invalid", 'details': serialized.errors}, status.HTTP_400_BAD_REQUEST)
        return Response({"error": "empty payload"}, status.HTTP_400_BAD_REQUEST)

    def get(self, request, national_id):
        try:
            queryset = m.Person.objects.get(national_id=national_id)
        except ObjectDoesNotExist:
            return Response({"msg": "object not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized = s.PersonResponseSerializer(queryset)
        return Response(serialized.data, status.HTTP_200_OK)

    def delete(self, request, national_id):
        qs = m.Person.objects.filter(national_id=national_id).first()
        if qs:
            qs.delete()
            return Response({"msg": "deleted"}, status.HTTP_200_OK)
        return Response({"msg": "not found"}, status.HTTP_404_NOT_FOUND)

    def put(self, request, national_id):
        pass

    def patch(self, request, national_id):
        pass

    def delete(self, request, national_id):
        pass

    @api_view(['GET'])
    def all_persons(request):
        persons_qs = m.Person.objects.all()
        serialized_data = s.PersonResponseSerializer(
            persons_qs, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)


class Student(APIView):
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id', None)
        if student_id:
            student = m.Student.objects.filter(id=student_id).first()
            if student:
                serialized_data = s.StudentResponseSerializer(
                    instance=student).data
                return Response(
                    {
                        "msg": "success",
                        "data": serialized_data
                    },
                    status=status.HTTP_200_OK
                )
            return Response({"msg": "student not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"msg": "student id is required"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        payload = request.data
        national_id = payload.get('national_id')
        if payload and national_id:
            emails = request.data.get('emails', [])
            phone_numbers = request.data.get('phone_numbers', [])
            addresses = request.data.get('addresses', [])

            # making emails, phone numbers, addresses objects
            emails_data = [{"email": email, "person": national_id}
                           for email in emails]
            phone_numbers_data = [
                {"number": phone, "person": national_id} for phone in phone_numbers]
            addresses_data = [{"address": address,
                               "person": national_id} for address in addresses]

            person_ser = s.PersonRequestSerializer(data=payload)
            if person_ser.is_valid():
                person_ser.save()
                payload['person'] = national_id
            else:
                return Response(
                    {
                        "msg": "failure",
                        "detail": person_ser.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            student_ser = s.StudentRequestSerializer(data=payload)
            email_ser = s.EmailSerializer(data=emails_data, many=True)
            phone_number_ser = s.PhoneNumberSerializer(
                data=phone_numbers_data, many=True)
            address_ser = s.AddressSerializer(data=addresses_data, many=True)

            is_all_valid = all([
                student_ser.is_valid(),
                phone_number_ser.is_valid(),
                address_ser.is_valid(),
                email_ser.is_valid()
            ])
            if is_all_valid:
                student_ser.save()
                phone_number_ser.save()
                address_ser.save()
                email_ser.save()

                # preparing student data for response display
                student = m.Student.objects.filter(
                    id=student_ser.data.get('id')).first()
                student_data = s.StudentResponseSerializer(student).data
                return Response(
                    {
                        "msg": "success",
                        "data": student_data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:

                m.Person.objects.get(national_id=national_id).delete()
                all_errors = {
                    "StudentInfo": student_ser.errors,
                    "Emails": email_ser.errors,
                    "PhoneNumbers": phone_number_ser.errors,
                    "Addresses": address_ser.errors,
                }

                return Response(
                    {
                        "msg": "failure",
                        "detail": all_errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {
                "msg": "failure",
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


@api_view(['GET', 'POST'])
def ClassAttendance_List(request):

    if request.method == 'GET':
        # get all the Attendances
        # serialize them
        # return json
        classAttendances = m.ClassAttendance.objects.all()
        serializer = s.ClassAttendanceSerializer(classAttendances, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        serializer = s.ClassAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ClassAttendance_List_detail(request, id):

    try:
        classAttendance = m.ClassAttendance.objects.get(pk=id)
    except m.ClassAttendance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = s.ClassAttendanceSerializer(classAttendance)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = s.ClassAttendanceSerializer(
            classAttendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        classAttendance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def StudentClass_list(request):

    if request.method == 'GET':
        studentClass = m.StudentClass.objects.all()
        serializer = s.StudentClassSerializer(studentClass, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        serializer = s.StudentClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def StudentClass_List_detail(request, id):

    try:
        studentClass = m.StudentClass.objects.get(pk=id)
    except m.StudentClass.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = s.StudentClassSerializer(studentClass)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = s.StudentClassSerializer(studentClass, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        studentClass.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Course_list(APIView):
    def post(self, request):
        data = request.data
        if data:
            serialized = s.CourseSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status.HTTP_201_CREATED)
            return Response({"error": "data is invalid", 'details': serialized.errors}, status.HTTP_400_BAD_REQUEST)
        return Response({"error": "empty payload"}, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            queryset = m.Course.objects.all()
        except ObjectDoesNotExist:
            return Response({"msg": "object not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized = s.CourseSerializer(queryset, many=True)
        return Response(serialized.data, status.HTTP_200_OK)


class Building(APIView):
    def get(self, request):
        qs = m.Building.objects.all()
        serialized = s.BuildingSerializer(qs, many=True)
        return Response(serialized.data, 200)

    def post(self, request):
        serializer = s.BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Room(APIView):
    def get(self, request):
        qs = m.Room.objects.all()
        serialized = s.RoomSerializer(qs, many=True)
        return Response(serialized.data, 200)

    def post(self, request):
        serializer = s.RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Department(APIView):
    def get(self, request):
        qs = m.Department.objects.all()
        serialized = s.DepartmentSerializer(qs, many=True)
        return Response(serialized.data, 200)

    def post(self, request):
        serializer = s.DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConstValue(APIView):
    def get(self, request):
        qs = m.ConstValue.objects.all()
        serialized = s.ConstValueSerializer(qs, many=True)
        return Response(serialized.data, 200)

    def post(self, request):
        serializer = s.ConstValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
