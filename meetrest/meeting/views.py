from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from .models import Stockholder, Student, Employee, Meeting, Membership, Proceeding, Resolution, ResolutionType
from django.db.models import Q
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import login, logout
from .serializers import *
from django.http import JsonResponse
from rest_framework.parsers import FileUploadParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
import datetime
from django.utils.dateparse import parse_date
# Import mimetypes module
import mimetypes
# Import HttpResponse module
from django.http.response import HttpResponse


import io
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import FileResponse
from reportlab.pdfgen import canvas
import arabic_reshaper
from bidi.algorithm import get_display


# Create your views here.
Daneshjou = 'دانشجو'
Karkonan = 'کارکنان'
class MeetingList(APIView):

    def get(self, request, format=None):
        if request.user.is_staff:
            qset = Meeting.objects.all()
        else:
            qset =  Meeting.meetings_user_belongs_to(request.user.id)
        serial_qset = MeetingNameSerializer(qset, many=True)
        # return a Json response
        return JsonResponse(serial_qset.data, safe=False)
    
    def post(self, request, format=None):
        serializer = MeetingOnlySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeetingDetail(APIView):

    def get_object(self, pk):
        try:
            return Meeting.objects.get(pk=pk)
        except Meeting.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        meeting = self.get_object(pk)
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        meeting = self.get_object(pk)
        serializer = MeetingOnlySerializer(meeting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        meeting = self.get_object(pk)
        meeting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MembershipList(APIView):

    def get(self, request, format=None):
        qset = Membership.objects.all()
        serial_qset = MembershipSerializer(qset, many=True)
        # return a Json response
        return JsonResponse(serial_qset.data, safe=False)
    
    def post(self, request, format=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MembershipDetail(APIView):

    def get_object(self, pk):
        try:
            return Membership.objects.get(pk=pk)
        except Membership.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        member = self.get_object(pk)
        serializer = MembershipSerializer(member)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        member = self.get_object(pk)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        member = self.get_object(pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EmployeeList(APIView):

    def get(self, request, format=None):
        meetingid = request.GET.get('meetingid', '')
        if (meetingid != ''):
            m = Meeting.objects.get(id=meetingid)
            qset = Employee.objects.filter(id__in=m.members.all())
        else:
            qset = Employee.objects.all()
        serial_qset = EmployeeSelectSerializer(qset, many=True)
        # return a Json response
        return JsonResponse(serial_qset.data, safe=False)
    
    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProceedingList(APIView):

    def get(self, request, format=None):
        meetingid = request.GET.get('meetingid', '')
        from_date = request.GET.get('fromdate', '')
        to_date = request.GET.get('todate', '')
        from_date = parse_date(from_date) if from_date != '' else datetime.date(1, 1, 1)
        to_date = parse_date(to_date) if to_date != '' else datetime.date.today()
        
        qset = Proceeding.objects.filter(meeting=meetingid, pdate__gte=from_date, pdate__lte=to_date)
        serial_qset = ProceedingNameSerializer(qset, many=True)
        # return a Json response
        return JsonResponse(serial_qset.data, safe=False)
    
    def post(self, request, format=None):
        print(request.data)
        serializer = ProceedingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProceedingDetail(APIView):

    def get_object(self, pk):
        try:
            return Proceeding.objects.get(pk=pk)
        except Proceeding.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        proceeding = self.get_object(pk)
        serializer = ProceedingSerializer(proceeding)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        proceeding = self.get_object(pk)
        serializer = ProceedingSerializer(proceeding, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        proceeding = self.get_object(pk)
        proceeding.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ResolutionList(APIView):

    def get(self, request, format=None):
        proceedingid = request.GET.get('proceedingid', '')
        qset = Resolution.objects.filter(proceeding=proceedingid)
        serial_qset = ResolutionZinafSerializer(qset, many=True)
        # return a Json response
        return JsonResponse(serial_qset.data, safe=False)
    
    def post(self, request, format=None):
        serializer = ResolutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResolutionDetail(APIView):

    def get_object(self, pk):
        try:
            return Resolution.objects.get(pk=pk)
        except Resolution.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        resolution = self.get_object(pk)
        serializer = ResolutionSerializer(resolution)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        resolution = self.get_object(pk)
        serializer = ResolutionSerializer(resolution, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        resolution = self.get_object(pk)
        resolution.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def resolve_stockholder(request):
    """ """
    stockholder_type = request.GET.get('stockholder_type', '')
    zinaf = request.GET.get('zinaf', '')
    if stockholder_type == Daneshjou:
        qset = Student.objects.get(stdno=zinaf)
        serial_qset = StudentNameIDSerializer(qset, many=False)
        return JsonResponse(serial_qset.data, safe=False)
    elif stockholder_type == Karkonan:
        qset = Stockholder.objects.get(national_id=zinaf)
        serial_qset = StockholderNameIDSerializer(qset, many=False)
        return JsonResponse(serial_qset.data, safe=False)
    return JsonResponse({}, status=400)

class ResolutionTypeList(APIView):

    def get(self, request, format=None):
        qset = ResolutionType.objects.all()
        serial_qset = ResolutionTypeSerializer(qset, many=True)
        # return a Json response
        return JsonResponse(serial_qset.data, safe=False)
    
    def post(self, request, format=None):
        serializer = ResolutionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchRes(APIView):
    def get(self, request, format=None):
        
        def _base_qset():
            if proceedingid and proceedingid != '0':
                return Resolution.objects.filter(proceeding=proceedingid)
            if meetingid and meetingid != '0':
                    qset = Resolution.objects.filter(proceeding__meeting=meetingid)
                    return qset.filter(proceeding__pdate__gte=from_date, proceeding__pdate__lte=to_date)
            meetings =  Meeting.meetings_user_belongs_to(request.user.id)
            qset = Resolution.objects.filter(proceeding__meeting__in=meetings)
            return qset.filter(proceeding__pdate__gte=from_date, proceeding__pdate__lte=to_date)

        meetingid = request.GET.get('meetingid', '')
        proceedingid = request.GET.get('proceedingid', '')
        restype = request.GET.get('restype', '')
        shtype = request.GET.get('shtype', '')
        searchtype = request.GET.get('searchtype', '')
        restext = request.GET.get('restext', '')
        from_date = request.GET.get('fromdate', '')
        to_date = request.GET.get('todate', '')
        from_date = parse_date(from_date) if from_date != '' else datetime.date(1, 1, 1)
        to_date = parse_date(to_date) if to_date != '' else datetime.date.today()
                
        qset =  _base_qset()

        if restype and restype!='0':
            qset = qset.filter(resolution_type=restype)
        if shtype and shtype!='0':
            qset = qset.filter(stockholder_type=shtype)
        
        # search by student no or national id
        if searchtype == 'NO':
            shno = request.GET.get('shno', '')
            if shtype == Daneshjou:
                try:
                    qset = qset.filter(stockholder_id=Student.objects.get(stdno=shno).id)
                except:
                    pass
            elif shtype == Karkonan:
                try:
                    qset = qset.filter(stockholder=Stockholder.objects.get(national_id=shno).id)
                except:
                    pass
        #search by first name or last name
        elif searchtype == 'NAME':
            shname = request.GET.get('shname', '')
            shname = shname.strip()
            qset = qset.select_related('stockholder').\
                    filter(Q(stockholder__first_name__contains=shname) | 
                           Q(stockholder__last_name__contains=shname))
        if restext != '':
            qset = qset.filter(act_text__contains=restext)                   
        serial_qset = ResolutionZinafSerializer(qset, many=True)
        return JsonResponse(serial_qset.data, safe=False)
        #paginator = PageNumberPagination()
        #context = paginator.paginate_queryset(queryset=qset, request=request)
        #serial_qset = ResolutionZinafSerializer(context, many=True)
        # return a Json response
        #return paginator.get_paginated_response(serial_qset.data)
        
def print_proceeding(request, pk):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    resolutions = Resolution.objects.filter(proceeding=pk)
    for res in resolutions:
        # reshape the text 
        item_no = arabic_reshaper.reshape(res.item_no)
        bidi_text = get_display(item_no)
        p.drawString(10, 100, bidi_text)

        act_text = arabic_reshaper.reshape(res.act_text)
        bidi_text = get_display(act_text)
        p.drawString(15, 100, bidi_text)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)
    @csrf_exempt
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class LogoutView(APIView):

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class StockholderDetail(APIView):

    def get_object(self):
        pk = self.request.user.id
        try:
            return Stockholder.objects.get(user=pk)
        except Stockholder.DoesNotExist:
            raise Http404
    def get(self, request, format=None):
        stockholder = self.get_object()
        serializer = stockholderSerializer(stockholder)
        return Response(serializer.data)

class FileUploadView(APIView):
    parser_classes = (FileUploadParser, )

    def post(self, request, meeting):

        up_file = request.FILES['file']
        try:
            os.mkdir(f'{settings.BASE_DIR}/meeting/assets/{meeting}/')
        except:
            pass
        #destination = open(f'{settings.BASE_DIR}/meeting/assets/{meeting}/{up_file.name}', 'wb+')
        destination = FileSystemStorage(location=f'{settings.BASE_DIR}/meeting/assets/{meeting}')
        filename = destination.save(up_file.name, up_file)
        #for chunk in up_file.chunks():
        #    destination.write(chunk)
        #destination.close()  # File should be closed only after all chuns are added
        #image = fs.url(filename)
        return Response(up_file.name, status.HTTP_201_CREATED)


def download_file(request, foldername, filename):
    # Define the full file path
    filepath = f"{settings.BASE_DIR}/meeting/assets/{foldername}/{filename}"
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response