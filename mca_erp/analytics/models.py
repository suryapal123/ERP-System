from django.db import models
from django.contrib.auth.models import User

# from django import forms


# Create your models here.
class Student(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    semester = models.IntegerField()


    def __str__(self):
        return self.name
    
class Subject(models.Model):

    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name
    
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    exam_type = models.CharField(
        max_length=20,
        choices=[
            ('MST1','MST-1'),
            ('MST2','MST-2'),
            ('FINAL','Final Exam')
        ]
    )
    marks = models.IntegerField()

    class Meta:
     unique_together = ('student','subject','exam_type')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.exam_type}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # attendance_percent = models.FloatField()
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[
            ('Present','Present'),
            ('Absent','Absent')
        ]
    )

    class Meta:
        unique_together = ('student','subject','date')

    def __str__(self):
        return f"{self.student} - {self.status}"
    

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class Schedule(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    semester = models.IntegerField()

    day = models.CharField(
        max_length=10,
        choices=[
            ('Monday','Monday'),
            ('Tuesday','Tuesday'),
            ('Wednesday','Wednesday'),
            ('Thursday','Thursday'),
            ('Friday','Friday'),
            ('Saturday','Saturday')
        ]
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.subject} - Sem {self.semester} - {self.day}"

# from django.contrib.auth.models import User
# from django.db import models


class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
