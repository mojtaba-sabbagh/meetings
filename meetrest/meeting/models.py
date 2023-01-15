from django.db import models
from django.contrib.auth.models import User
from jalali_date import date2jalali
# Create your models here.

class Stockholder(models.Model):
    GENDER_CHOICES = (
        ('M', 'مرد'),
        ('F', 'زن'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICES)
    birthday = models.DateField(blank=True, null=True)
    national_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    #class Meta:
        #abstract = True

class Student(models.Model):
    MAGHTA_CHOICES = (
        ('کارشناسی', 'کارشناسی'),
        ('کارشناسی ارشد', 'کارشناسی ارشد'),
        ('دکتری', 'دکتری')
    )
    stockholder = models.OneToOneField(Stockholder, on_delete=models.CASCADE)
    stdno = models.CharField(max_length=10, unique=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    maghta = models.CharField(max_length=20, default='کارشناسی', choices=MAGHTA_CHOICES)
    
    def __str__(self):
        return f"{self.stdno} - {self.stockholder}"

class Employee(models.Model):
    TYPE_CHOICE = (
        ('کارمند', 'کارمند'),
        ('هیات علمی', 'هیات علمی'),
    )
    stockholder = models.OneToOneField(Stockholder, on_delete=models.CASCADE)
    employee_no = models.CharField(max_length=10, unique=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, default='کارمند', choices=TYPE_CHOICE)
    dep = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.employee_no} - {self.stockholder}"

class Meeting(models.Model):
    PERIOD_CHOICE = (
        ('روزانه', 'روزانه'),
        ('هفتگی', 'هفتگی'),
        ('دوهفتگی', 'هفتگی'),
        ('ماهیانه', 'ماهیانه'),
        ('غیرمشخص', 'غیرمشخص'),
    )
    meeting_name = models.CharField(max_length=255)
    period = models.CharField(max_length=255, blank=True, null=True, choices=PERIOD_CHOICE)
    members = models.ManyToManyField(Employee, through='Membership')

    def is_member(self, user):
        # check if 'user' is member of the meeting.
        for member in self.members.all():
            if member.stockholder.user.id == user:
                return True
        return False
    
    @staticmethod
    def meetings_user_belongs_to(user):
        meetings = []
        all_meetings = Meeting.objects.all()
        for meeting in all_meetings:
            if meeting.is_member(user):
                meetings.append(meeting)
        return meetings
    
    def __str__(self):
        return self.meeting_name

class Membership(models.Model):
    ROLE_CHOICE = (
        ('عضو', 'عضو'),
        ('دبیر', 'دبیر'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=ROLE_CHOICE)

    def __str__(self):
        return f"{self.employee} - {self.role} {self.meeting}"

class Proceeding(models.Model):
    proceeding_no = models.CharField(max_length=255)
    pdate = models.DateField()
    ptime = models.TimeField(blank=True, null=True)
    loc = models.CharField(max_length=255, blank=True, null=True)
    participants =  models.ManyToManyField(Employee)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    readonly = models.BooleanField(default=False)
    upload = models.FileField(upload_to ='proceedings/', blank=True, null=True)

    def __str__(self):
        return f"{self.meeting} - {self.proceeding_no} - {date2jalali(self.pdate).strftime('%Y/%m/%d')}"

class Resolution(models.Model):
    STOCKHOLDER_CHOICE = (
        ('دانشجو', 'دانشجو'),
        ('کارکنان', 'کارکنان'),
    )
    item_no = models.CharField(max_length=64)
    act_text = models.CharField(max_length=255)
    resolution_type = models.CharField(max_length=255, blank=True, null=True)
    result = models.BooleanField(default=True)
    proceeding = models.ForeignKey(Proceeding, on_delete=models.CASCADE)
    stockholder_type = models.CharField(max_length=64, choices=STOCKHOLDER_CHOICE)
    stockholder = models.ForeignKey(Stockholder, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.item_no} - {self.proceeding}"

class ResolutionType(models.Model):
     resolution_type = models.CharField(max_length=255)
     def __str__(self):
        return self.resolution_type