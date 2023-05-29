from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


from amuzeshyar import (
    serializers as s,
    models as m
)


@extend_schema(
    tags=["Person"]
)
class PersonList(APIView):
    @extend_schema(
        summary="HAYA",
        request=None,
        responses={
            200: s.PersonResponseSerializer
        },

    )
    def get(self, request):
        persons_qs = m.Person.objects.all()
        serialized_data = s.PersonResponseSerializer(
            persons_qs, many=True).data
        return Response(serialized_data, status.HTTP_200_OK)

    @extend_schema(
        request=s.PersonRequestSerializer,
        responses={
            201: s.PersonRequestSerializer
        },
    )
    def post(self, request):
        data = request.data
        if data:
            serialized = s.PersonRequestSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status.HTTP_201_CREATED)
            return Response({"error": "data is invalid", 'details': serialized.errors}, status.HTTP_400_BAD_REQUEST)
        return Response({"error": "empty payload"}, status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Person"])
class PersonDetail(APIView):

    @extend_schema(
        request=None,
        responses={
            200: s.PersonResponseSerializer,
        }
    )
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
        return Response(status=501)

    def patch(self, request, national_id):
        return Response(status=501)

    def delete(self, request, national_id):
        return Response(status=501)


@extend_schema(tags=["Student"])
class StudentList(APIView):
    def get(self, request):
        return Response(status=501)

    @extend_schema(
        request=s.StudentRequestSerializer,
        responses={
            200: s.StudentResponseSerializer,
        }
    )
    def post(self, request):
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


@extend_schema(tags=["Student"])
class StudentDetail(APIView):
    @extend_schema(
        request=None,
        responses={
            200: s.StudentResponseSerializer
        }
    )
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

    def put(self, request, *args, **kwargs):
        return Response(status=501)

    def patch(self, request, *args, **kwargs):
        return Response(status=501)

    def delete(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id', None)
        if student_id:
            student = m.Student.objects.filter(id=student_id).first()
            person = student.person
            if student:
                # Delete related objects first
                m.Email.objects.filter(person=person).delete()
                m.PhoneNumber.objects.filter(person=person).delete()
                m.Address.objects.filter(person=person).delete()

                # Delete the student object
                student.delete()
                return Response({"msg": "Success"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"msg": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"msg": "Student id is required"}, status=status.HTTP_400_BAD_REQUEST)({"msg": "student id is required"}, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    def get_students(request, *args, **kwargs):
        return Response(status=501)


@extend_schema(
    request=s.ClassAttendanceSerializer,
    responses={
        status.HTTP_200_OK: s.ClassAttendanceSerializer(many=True),
    },
    summary="List or create ClassAttendances",
    tags=["Class Attendance",])
@api_view(['GET', 'POST'])
def ClassAttendance_List(request):

    if request.method == 'GET':
        # get all the Attendances
        # serialize them
        # return json
        classAttendances = m.ClassAttendance.objects.all()
        serializer = s.ClassAttendanceSerializer(classAttendances, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = s.ClassAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(

    request=s.ClassAttendanceSerializer,
    responses={
        status.HTTP_200_OK: s.ClassAttendanceSerializer,
    },

    tags=["Class Attendance",])
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


@extend_schema(
    request=s.StudentClassSerializer,
    responses={
        status.HTTP_200_OK: s.StudentClassSerializer(),
    },
    tags=["Class Registration"])
@api_view(['GET', 'POST'])
def StudentClass_list(request):

    if request.method == 'GET':
        studentClass = m.StudentClass.objects.all()
        serializer = s.StudentClassSerializer(studentClass, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = s.StudentClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=s.StudentClassSerializer,
    responses={
        status.HTTP_200_OK: s.StudentClassSerializer,
    },
    tags=["Class Registration"])
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


@extend_schema(tags=["Course"])
class Course_list(APIView):
    @extend_schema(
        request=s.CourseSerializer,
        responses={status.HTTP_201_CREATED: s.CourseSerializer},
    )
    def post(self, request):
        data = request.data
        if data:
            serialized = s.CourseSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status.HTTP_201_CREATED)
            return Response({"error": "data is invalid", 'details': serialized.errors}, status.HTTP_400_BAD_REQUEST)
        return Response({"error": "empty payload"}, status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={status.HTTP_200_OK: s.CourseSerializer(many=True)},
    )
    def get(self, request):
        try:
            queryset = m.Course.objects.all()
        except ObjectDoesNotExist:
            return Response({"msg": "object not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized = s.CourseSerializer(queryset, many=True)
        return Response(serialized.data, status.HTTP_200_OK)

class CourseDetail(RetrieveUpdateDestroyAPIView):
   queryset = m.Course.objects.all()
   serializer_class = s.CourseSerializer

@extend_schema(tags=["Place"])
class Building(APIView):
    @extend_schema(
        request=s.BuildingSerializer,
        responses={
            200: s.BuildingSerializer
        }
    )
    def get(self, request):
        qs = m.Building.objects.all()
        serialized = s.BuildingSerializer(qs, many=True)
        return Response(serialized.data, 200)

    @extend_schema(
        request=s.BuildingSerializer,
        responses={
            201: s.BuildingSerializer
        }
    )
    def post(self, request):
        serializer = s.BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=s.BuildingSerializer,
    responses={
        status.HTTP_200_OK: s.BuildingSerializer,
    },
    tags=["Place"])
@api_view(['GET', 'PUT', 'DELETE'])
def Building_List_detail(request, id):

    try:
        building = m.Building.objects.get(pk=id)
    except m.Building.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = s.BuildingSerializer(building)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = s.BuildingSerializer(building, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        building.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=["Place"])
class Room(APIView):
    @extend_schema(
        request=None,
        responses={
            200: s.RoomSerializer
        }
    )
    def get(self, request):
        qs = m.Room.objects.all()
        serialized = s.RoomSerializer(qs, many=True)
        return Response(serialized.data, 200)

    @extend_schema(
        request=s.RoomSerializer,
        responses={
            201: s.RoomSerializer
        }
    )
    def post(self, request):
        serializer = s.RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=s.RoomSerializer,
    responses={
        status.HTTP_200_OK: s.RoomSerializer,
    },
    tags=["Place"])
@api_view(['GET', 'PUT', 'DELETE'])
def Room_List_detail(request, code):

    try:
        room = m.Room.objects.get(pk=code)
    except m.Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = s.RoomSerializer(room)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = s.RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=["Department"])
class DepartmentList(ListCreateAPIView):
    queryset = m.Department.objects.all()
    serializer_class = s.DepartmentSerializer


@extend_schema(tags=["Department"])
class DepartmentDetail(RetrieveUpdateDestroyAPIView):
    queryset = m.Department.objects.all()
    serializer_class = s.DepartmentSerializer


@extend_schema(tags=["ConstValue"])
class ConstValueList(ListCreateAPIView):
    queryset = m.ConstValue.objects.all()
    serializer_class = s.ConstValueSerializer


@extend_schema(tags=["ConstValue"])
class ConstValueDetail(RetrieveUpdateDestroyAPIView):
    queryset = m.ConstValue.objects.all()
    serializer_class = s.ConstValueSerializer


@api_view(['GET', 'POST'])
def FixedTuitionFee_List(request):

    if request.method == 'GET':
        qs = m.FixedTuitionFee.objects.all()
        serializer = s.FixedTuitionFeeSerializer(qs, many=True)
        return Response(serializer.data, 200)
    if request.method == 'POST':
        payload = request.data
        if payload:
            serializer = s.FixedTuitionFeeSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 201)
            return Response(serializer.errors, 400)
        return Response({"msg": "Payload Required"}, 400)


@api_view(['GET', 'PUT', 'DELETE'])
def FixedTuitionFee_Detail(request, id):

    try:
        fee = m.FixedTuitionFee.objects.get(pk=id)
    except m.FixedTuitionFee.DoesNotExist:
        return Response(404)
    if request.method == 'GET':
        serializer = s.FixedTuitionFeeSerializer(fee)
        return Response(serializer.data)
        pass
    elif request.method == 'PUT':
        serializer = s.FixedTuitionFeeSerializer(fee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return  Response(serializer.errors, 400)
        pass
    elif request.method == 'DELETE':
        fee.delete()
        return Response(204)
@api_view(['GET', 'POST'])
def SemesterCourseTuition_List(request):

    if request.method == 'GET':
        qs = m.SemesterCourseTuition.objects.all()
        serializer = s.SemesterCourseTuitionSerializer(qs, many=True)
        return Response(serializer.data, 200)
    if request.method == 'POST':
        payload = request.data
        if payload:
            serializer = s.SemesterCourseTuitionSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 201)
            return Response(serializer.errors, 400)
        return Response({"msg": "Payload Required"}, 400)


@api_view(['GET', 'PUT', 'DELETE'])
def SemesterCourseTuition_Detail(request, id):

    try:
        tuition = m.SemesterCourseTuition.objects.get(pk=id)
    except m.SemesterCourseTuition.DoesNotExist:
        return Response(404)
    if request.method == 'GET':
        serializer = s.SemesterCourseTuitionSerializer(tuition)
        return Response(serializer.data)
        pass
    elif request.method == 'PUT':
        serializer = s.SemesterCourseTuitionSerializer(tuition, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return  Response(serializer.errors, 400)
        pass
    elif request.method == 'DELETE':
        tuition.delete()
        return Response(204)
@api_view(['GET', 'POST'])
def StudentPayment_List(request):

    if request.method == 'GET':
        qs = m.StudentPayment.objects.all()
        serializer = s.StudentPaymentSerializer(qs, many=True)
        return Response(serializer.data, 200)
    if request.method == 'POST':
        payload = request.data
        if payload:
            serializer = s.StudentPaymentSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 201)
            return Response(serializer.errors, 400)
        return Response({"msg": "Payload Required"}, 400)


@api_view(['GET', 'PUT', 'DELETE'])
def StudentPayment_Detail(request, id):

    try:
        payment = m.StudentPayment.objects.get(pk=id)
    except m.StudentPayment.DoesNotExist:
        return Response(404)
    if request.method == 'GET':
        serializer = s.StudentPaymentSerializer(payment)
        return Response(serializer.data)
        pass
    elif request.method == 'PUT':
        serializer = s.StudentPaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return  Response(serializer.errors, 400)
        pass
    elif request.method == 'DELETE':
        payment.delete()
        return Response(204)
@api_view(['GET', 'POST'])
def StudentInvoice_List(request):

    if request.method == 'GET':
        qs = m.StudentInvoice.objects.all()
        serializer = s.StudentInvoiceSerializer(qs, many=True)
        return Response(serializer.data, 200)
    if request.method == 'POST':
        payload = request.data
        if payload:
            serializer = s.StudentInvoiceSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 201)
            return Response(serializer.errors, 400)
        return Response({"msg": "Payload Required"}, 400)


@api_view(['GET', 'PUT', 'DELETE'])
def StudentInvoice_Detail(request, id):

    try:
        invoice = m.StudentInvoice.objects.get(pk=id)
    except m.StudentInvoice.DoesNotExist:
        return Response(404)
    if request.method == 'GET':
        serializer = s.StudentInvoiceSerializer(invoice)
        return Response(serializer.data)
        pass
    elif request.method == 'PUT':
        serializer = s.StudentInvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return  Response(serializer.errors, 400)
        pass
    elif request.method == 'DELETE':
        invoice.delete()
        return Response(204)

@api_view(['GET', 'POST'])
def Announcement_List(request):

    if request.method == 'GET':
        qs = m.Announcement.objects.all()
        serializer = s.AnnouncementSerializer(qs, many=True)
        return Response(serializer.data, 200)
    if request.method == 'POST':
        payload = request.data
        if payload:
            serializer = s.AnnouncementSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 201)
            return Response(serializer.errors, 400)
        return Response({"msg": "Payload Required"}, 400)


@api_view(['GET', 'PUT', 'DELETE'])
def Announcement_Detail(request, id):

    try:
        ann = m.Announcement.objects.get(pk=id)
    except m.Announcement.DoesNotExist:
        return Response(404)
    if request.method == 'GET':
        serializer = s.AnnouncementSerializer(ann)
        return Response(serializer.data)
        pass
    elif request.method == 'PUT':
        serializer = s.AnnouncementSerializer(ann, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return  Response(serializer.errors, 400)
        pass
    elif request.method == 'DELETE':
        ann.delete()
        return Response(204)
@api_view(['GET', 'POST'])
def AnnouncementText_List(request):

    if request.method == 'GET':
        qs = m.AnnouncementText.objects.all()
        serializer = s.AnnouncementTextSerializer(qs, many=True)
        return Response(serializer.data, 200)
    if request.method == 'POST':
        payload = request.data
        if payload:
            serializer = s.AnnouncementTextSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 201)
            return Response(serializer.errors, 400)
        return Response({"msg": "Payload Required"}, 400)


@api_view(['GET', 'PUT', 'DELETE'])
def AnnouncementText_Detail(request, id):

    try:
        ann = m.AnnouncementText.objects.get(pk=id)
    except m.AnnouncementText.DoesNotExist:
        return Response(404)
    if request.method == 'GET':
        serializer = s.AnnouncementTextSerializer(ann)
        return Response(serializer.data)
        pass
    elif request.method == 'PUT':
        serializer = s.AnnouncementTextSerializer(ann, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 201)
        return  Response(serializer.errors, 400)
        pass
    elif request.method == 'DELETE':
        ann.delete()
        return Response(204)

@extend_schema(tags=["Semester"])
class Semester(APIView):
    def get(self, request, id):
        qs = m.Semester.objects.filter(id=id).first()
        if qs:
            SerializedData = s.SemesterSerializer(qs).data
            return Response(SerializedData, status=status.HTTP_200_OK)
        return Response({"msg": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        payload = request.data
        if payload:
            Serialized = s.SemesterSerializer(data=payload)
            if Serialized.is_valid():
                Serialized.save()
                return Response(Serialized.data, status=status.HTTP_201_CREATED)
            return Response(Serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Payload Required"}, 400)

    @api_view(['GET'])
    def Semester_List_detail(request):
        qs = m.Semester.objects.all()
        serialized = s.SemesterSerializer(qs, many=True)
        return Response(serialized.data, 200)
    
    def delete(self, request, id):
        qs = m.Semester.objects.filter(id=id).first()
        if qs:
            qs.delete()
            return Response({"msg": "deleted"}, status.HTTP_200_OK)
        return Response({"msg": "not found"}, status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        pass

    def patch(self, request, id):
        pass

@extend_schema(tags=["Class"])
class Class(APIView):
    def get(self, request, id):
        qs = m.Class.objects.filter(id=id).first()
        if qs:
            SerializedData = s.ClassSerializer(qs).data
            return Response(SerializedData, status=status.HTTP_200_OK)
        return Response({"msg": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        payload = request.data
        if payload:
            Serialized = s.ClassSerializer(data=payload)
            if Serialized.is_valid():
                Serialized.save()
                return Response(Serialized.data, status=status.HTTP_201_CREATED)
            return Response(Serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Payload Required"}, 400)

    @api_view(['GET'])
    def Class_List_detail(request):
        qs = m.Class.objects.all()
        serialized = s.ClassSerializer(qs, many=True)
        return Response(serialized.data, 200)
    
    def delete(self, request, id):
        qs = m.Class.objects.filter(id=id).first()
        if qs:
            qs.delete()
            return Response({"msg": "deleted"}, status.HTTP_200_OK)
        return Response({"msg": "not found"}, status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        pass

    def patch(self, request, id):
        pass


@extend_schema(tags=["ClassSchedule"])
class ClassSchedule(APIView):
    def get(self, request, id):
        qs = m.ClassSchedule.objects.filter(id=id).first()
        if qs:
            SerializedData = s.ClassScheduleSerializer(qs).data
            return Response(SerializedData, status=status.HTTP_200_OK)
        return Response({"msg": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        payload = request.data
        if payload:
            Serialized = s.ClassScheduleSerializer(data=payload)
            if Serialized.is_valid():
                Serialized.save()
                return Response(Serialized.data, status=status.HTTP_201_CREATED)
            return Response(Serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "Payload Required"}, 400)

    @api_view(['GET'])
    def ClassSchedule_List_detail(request):
        qs = m.ClassSchedule.objects.all()
        serialized = s.ClassScheduleSerializer(qs, many=True)
        return Response(serialized.data, 200)
    
    def delete(self, request, id):
        qs = m.ClassSchedule.objects.filter(id=id).first()
        if qs:
            qs.delete()
            return Response({"msg": "deleted"}, status.HTTP_200_OK)
        return Response({"msg": "not found"}, status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        pass

    def patch(self, request, id):
        pass

class Specialization(APIView):
    def post(self, request):
        data = request.data
        if data:
            serialized = s.SpecializationSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status.HTTP_201_CREATED)
            return Response({"error": "data is invalid", 'details': serialized.errors}, status.HTTP_400_BAD_REQUEST)
        return Response({"error": "empty payload"}, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            queryset = m.SpecializationModel.objects.all()
        except ObjectDoesNotExist:
            return Response({"msg": "object not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized = s.SpecializationSerializer(queryset,many=True)
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



class Specialization(APIView):
   def post(self, request):
       data = request.data
       if data:
           serialized = s.SpecializationSerializer(data=data)
           if serialized.is_valid():
               serialized.save()
               return Response(serialized.data, status.HTTP_201_CREATED)
           return Response({"error": "data is invalid", 'details': serialized.errors}, status.HTTP_400_BAD_REQUEST)
       return Response({"error": "empty payload"}, status.HTTP_400_BAD_REQUEST)

   def get(self, request):
       try:
           queryset = m.Specialization.objects.all()
       except ObjectDoesNotExist:
           return Response({"msg": "object not found"}, status=status.HTTP_404_NOT_FOUND)
       serialized = s.SpecializationSerializer(queryset,many=True)
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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def first_page(request, student_id):
    
    qs = m.Student.objects.filter(id = student_id).first()
    serialized_data = s.FirstPageInformationSerializer(qs, context={"current_term":request.query_params.get("term")})
    return Response(serialized_data.data, status.HTTP_200_OK)
    