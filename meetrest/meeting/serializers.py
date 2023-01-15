from rest_framework import serializers
from .models import Stockholder, Student, Employee, Meeting, Membership, Proceeding, Resolution, ResolutionType
from jalali_date import date2jalali

from django.contrib.auth import authenticate
from rest_framework import serializers

Daneshjou = 'دانشجو'
Karkonan = 'کارکنان'

class FullnameField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.first_name} {value.last_name}"

"""
class StockhoderField(serializers.RelatedField):
    def to_representation(self, value):
        return value.title

class DutiesField(serializers.RelatedField):
    def to_representation(self, value):
        return value.duties
"""
class MeetingNameSerializer(serializers.ModelSerializer):
    ID = serializers.IntegerField(read_only=True, source="id")
    text = serializers.CharField(source='meeting_name', read_only=True)
    class Meta:
        model = Meeting
        fields = (
            'ID',
            'text',
        )

class ProceedingNameSerializer(serializers.ModelSerializer):
    ID = serializers.IntegerField(read_only=True, source="id")
    text = serializers.SerializerMethodField()
    def get_text(self, obj):
        return f"{obj.proceeding_no} - {date2jalali(obj.pdate).strftime('%Y/%m/%d')}"
    class Meta:
        model = Proceeding
        fields = (
            'ID',
            'text',
        )


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ProceedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proceeding
        fields = '__all__'
        
class ResolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resolution
        fields = '__all__'

class MembershipSerializer(serializers.ModelSerializer):
    employee_fullname = FullnameField(source='employee.stockholder', read_only=True)
    employee_id = serializers.ReadOnlyField(source='employee.id', read_only=True)
    national_id = serializers.ReadOnlyField(source='employee.stockholder.national_id')
    role = serializers.CharField(read_only=True)
    class Meta:
        model = Membership
        fields = ('id', 'role', 'employee_fullname', 'employee_id', 'national_id')

class StockholderNameIDSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    def get_fullname(self, obj):
        return f"{obj.first_name} - {obj.last_name}"
    stockholder = serializers.ReadOnlyField(source='id', read_only=True)
    gender = serializers.ReadOnlyField()
    class Meta:
        model = Stockholder
        fields = ('fullname', 'stockholder', 'gender')

class StudentNameIDSerializer(serializers.ModelSerializer):
    fullname = FullnameField(source='stockholder', read_only=True)
    stockholder = serializers.ReadOnlyField(source='stockholder.id', read_only=True)
    gender = serializers.ReadOnlyField(source='stockholder.gender')
    class Meta:
        model = Student
        fields = ('stockholder', 'fullname', 'gender')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class EmployeeSelectSerializer(serializers.ModelSerializer):
    ID = serializers.ReadOnlyField(source='id', read_only=True)
    text = FullnameField(source='stockholder', read_only=True)
    class Meta:
        model = Employee
        fields = ('ID', 'text')

class MeetingSerializer(serializers.ModelSerializer):
    # 
    members = MembershipSerializer(source='membership_set', many=True, read_only=True)
    class Meta:
        model = Meeting
        fields = (
            'id',
            'meeting_name',
            'period',
            'members',
            )

class MeetingOnlySerializer(serializers.ModelSerializer):
    # 
    class Meta:
        model = Meeting
        fields = (
            'meeting_name',
            'period',
            )

class ResolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resolution
        fields = '__all__'

class ResolutionTypeSerializer(serializers.ModelSerializer):
    ID = serializers.IntegerField(read_only=True, source="id")
    text = serializers.ReadOnlyField(read_only=True, source="resolution_type")
    class Meta:
        model = ResolutionType
        fields = (
            'ID',
            'text',
        )
class ResolutionZinafSerializer(serializers.ModelSerializer):
    meeting = serializers.SerializerMethodField()
    def get_meeting(self, obj):
        return obj.proceeding.meeting.meeting_name
    zinaf = serializers.SerializerMethodField()
    def get_zinaf(self, obj):
        if obj.stockholder_type == Daneshjou:
            student = Student.objects.get(stockholder=obj.stockholder.id)
            return student.stdno
        elif obj.stockholder_type == Karkonan:
            stockholder = Stockholder.objects.get(id=obj.stockholder.id)
            return stockholder.national_id
        return ''
    fullname = serializers.SerializerMethodField()
    def get_fullname(self, obj):
        return f"{obj.stockholder.first_name} {obj.stockholder.last_name}"
    gender = serializers.SerializerMethodField()
    def get_gender(self, obj):
        return obj.stockholder.gender
    proceedingdate = serializers.SerializerMethodField()
    def get_proceedingdate(self, obj):
        return date2jalali(obj.proceeding.pdate).strftime('%Y/%m/%d')
    class Meta:
        model = Resolution
        fields = ('id','item_no', 'act_text','resolution_type', 'result', 'proceeding', 'stockholder_type',
                  'stockholder', 'zinaf', 'fullname', 'gender', 'meeting', 'proceedingdate')

class stockholderSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self, obj):
        return obj.user.username
        
    class Meta:
        model = Stockholder
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]
"""
class DepNameSerializer(serializers.ModelSerializer):
    # PrimaryKeyRelatedField
    ID = serializers.IntegerField(read_only=True, source="id")
    text = serializers.SerializerMethodField()
    def get_text(self, obj):
        return f'{obj.dep_title} {obj.dep_name}'

    class Meta:
        model = Department
        fields = (
            'ID',
            'text',
        )
"""

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs