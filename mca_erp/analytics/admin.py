from django.contrib import admin
from .models import Student,Subject,Marks,Attendance
from.models import Teacher
from .models import Schedule
from .models import UserProfile

admin.site.register(UserProfile)

admin.site.register(Schedule)
# Register your models here.
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Marks)
admin.site.register(Attendance)
admin.site.register(Teacher)
