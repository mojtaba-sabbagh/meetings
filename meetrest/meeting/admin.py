from django.contrib import admin
# Register your models here.

from .models import Stockholder, Student, Employee, Meeting, Membership, Proceeding, Resolution, ResolutionType

@admin.register(Stockholder)
class StockholderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(Proceeding)
class ProceedingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(Resolution)
class ResolutionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(ResolutionType)
class ResolutionTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

