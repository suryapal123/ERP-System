from django.shortcuts import render,redirect
from .models import Student,Marks,Attendance,Subject
from django.db.models import Avg
# from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from .models import Marks
from .forms import MarksForm
from datetime import date
from django.db.models import Count
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .forms import StudentSignupForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from .models import Teacher
from datetime import datetime
from .models import Student, Marks, Attendance, Schedule
from .models import UserProfile
import random
from django.core.mail import send_mail
import time


# Create your views here.
def home(request):
    return render(request,'home.html')

def is_staff(user):
    return user.is_staff

@login_required
def student_dashboard(request):

    student = Student.objects.get(user=request.user)

    attendance_records = Attendance.objects.filter(student=student)

    total_classes = attendance_records.count()
    present_classes = attendance_records.filter(status="Present").count()
    absent_classes = attendance_records.filter(status="Absent").count()

    if total_classes > 0:
        attendance_percentage = (present_classes / total_classes) * 100
    else:
        attendance_percentage = 0

    today = datetime.today().strftime('%A')

    todays_classes = Schedule.objects.filter(
        day=today,
        semester=student.semester
    )

    todays_attendance = Attendance.objects.filter(
        student=student,
        date=date.today()
    )

    context = {
        "student": student,
        "attendance_percentage": round(attendance_percentage,2),
        "present_classes": present_classes,
        "absent_classes": absent_classes,
        "todays_classes": todays_classes,
        "todays_attendance": todays_attendance
    }

    return render(request,"student_dashboard.html",context)

#     total_students = Student.objects.count()
#     total_subjects = Subject.objects.count()

#     avg_marks = Marks.objects.aggregate(Avg('marks'))['marks__avg']

#     context = {
#         'total_students': total_students,
#         'total_subjects': total_subjects,
#         'avg_marks': avg_marks
#     }

#     return render(request, 'admin_dashboard.html', context)

# def admin_dashboard(request):

#     students = Student.objects.all()

#     names = []
#     marks = []

#     for s in students:
#         student_marks = Marks.objects.filter(student=s).aggregate(Avg('marks'))['marks__avg']
        
#         if student_marks:
#             names.append(s.name)
#             marks.append(student_marks)

#     avg_marks = Marks.objects.aggregate(Avg('marks'))['marks__avg']

#     if avg_marks is None:
#         avg_marks = 0

#     context = {
#         'names': names,
#         'marks': marks,
#         'total_students': Student.objects.count(),
#         'total_subjects': Subject.objects.count(),
#         'avg_marks' : avg_marks
#     }

#     return render(request,'admin_dashboard.html',context)

# from django.shortcuts import render
# from django.db.models import Avg
# from .models import Student, Marks, Subject, Attendance


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required


@login_required
def admin_dashboard(request):

    # If user is not teacher/admin redirect to student dashboard
    if not request.user.is_staff:
        return redirect('student_dashboard')

    students = Student.objects.all()

    names = []
    marks = []

    student_names = []
    attendance_percentages = []
    low_attendance = []

    # MARKS ANALYSIS
    for s in students:

        student_marks = Marks.objects.filter(student=s).aggregate(Avg('marks'))['marks__avg']

        if student_marks is not None:
            names.append(s.name)
            marks.append(round(student_marks,2))

    avg_marks = Marks.objects.aggregate(Avg('marks'))['marks__avg']

    if avg_marks is None:
        avg_marks = 0

    # ATTENDANCE DISTRIBUTION
    present_count = Attendance.objects.filter(status="Present").count()
    absent_count = Attendance.objects.filter(status="Absent").count()

    # ATTENDANCE PERCENTAGE
    for student in students:

        total_classes = Attendance.objects.filter(student=student).count()

        present_classes = Attendance.objects.filter(
            student=student,
            status="Present"
        ).count()

        if total_classes > 0:
            percentage = (present_classes / total_classes) * 100
        else:
            percentage = 0

        student_names.append(student.name)
        attendance_percentages.append(round(percentage,2))

        if percentage < 75:
            low_attendance.append({
                "name": student.name,
                "percentage": round(percentage,2)
            })

    context = {

        'students': students,

        'names': names,
        'marks': marks,
        'avg_marks': avg_marks,

        'total_students': Student.objects.count(),
        'total_subjects': Subject.objects.count(),

        'present_count': present_count,
        'absent_count': absent_count,

        'student_names': student_names,
        'attendance_percentages': attendance_percentages,
        'low_attendance': low_attendance,
    }

    return render(request, 'admin_dashboard.html', context)

def student_list(request):

    students = Student.objects.all()

    return render(request,'student_list.html',{'students':students})

def add_student(request):

    form = StudentForm()

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Student Added Successfully!")

            return redirect('add_student')

    return render(request,'add_student.html',{'form':form})

def edit_student(request,id):

    student = Student.objects.get(id=id)

    form = StudentForm(instance=student)

    if request.method == 'POST':

        form = StudentForm(request.POST,instance=student)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    return render(request,'add_student.html',{'form':form})

def delete_student(request,id):

    student = Student.objects.get(id=id)

    student.delete()

    return redirect('student_list')


# def add_marks(request):

#     form = MarksForm()

#     if request.method == "POST":

#         form = MarksForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('admin_dashboard')

#     return render(request,'add_marks.html',{'form':form})

def marks_dashboard(request):

    records = Marks.objects.all()

    students = []
    marks = []

    for r in records:
        students.append(r.student.name + "("+ r.exam_type + ")")
        marks.append(r.marks)

    context = {
        "students": students,
        "marks": marks,
        "records": records
    }

    return render(request,'marks_dashboard.html',context)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Subject, Attendance


def mark_attendance(request):

    students = Student.objects.all()
    subjects = Subject.objects.all()

    if request.method == "POST":

        subject_id = request.POST.get("subject")
        attendance_date = request.POST.get("date")

        if not subject_id or not attendance_date:
            messages.warning(request, "Please select subject and date")
            return redirect("mark_attendance")

        attendance_saved = False

        for student in students:

            status = request.POST.get(f"status_{student.id}")

            if not status:
                continue

            exists = Attendance.objects.filter(
                student=student,
                subject_id=subject_id,
                date=attendance_date
            ).exists()

            if exists:
                messages.warning(
                    request,
                    f"Attendance already marked!"
                )
                continue

            Attendance.objects.create(
                student=student,
                subject_id=subject_id,
                date=attendance_date,
                status=status
            )

            attendance_saved = True

        if attendance_saved:
            messages.success(request, "Attendance saved successfully")

        return redirect("mark_attendance")

    return render(request, "mark_attendance.html", {
        "students": students,
        "subjects": subjects
    })

def attendance_history(request):
    records = Attendance.objects.all().order_by('-date')


    students = Student.objects.all()
    subjects = Subject.objects.all()


    student_id = request.GET.get('student')
    subject_id = request.GET.get('subject')
    date = request.GET.get('date')

    if student_id:
        records = records.filter(student_id=student_id)

    if subject_id:
        records = records.filter(subject_id=subject_id)

    if date:
        records = records.filter(date=date)

    context = {
        'records': records,
        'students': students,
        'subjects': subjects
    }

    return render(request,'attendance_history.html',context)

# from django.contrib import messages


def add_marks(request):

    form = MarksForm()

    if request.method == "POST":

        form = MarksForm(request.POST)

        if form.is_valid():

            student = form.cleaned_data['student']
            subject = form.cleaned_data['subject']
            exam_type = form.cleaned_data['exam_type']

            exists = Marks.objects.filter(
                student=student,
                subject=subject,
                exam_type=exam_type
            ).exists()

            if exists:
                messages.warning(request,"Marks already added for this exam")
                return redirect('add_marks')

            form.save()

            messages.success(request,"Marks saved successfully")

            return redirect('marks_dashboard')

    return render(request,'add_marks.html',{'form':form})



def result_dashboard(request):

    students = Student.objects.all()

    results = []

    for student in students:

        mst1 = Marks.objects.filter(student=student, exam_type="MST1").aggregate(Sum('marks'))['marks__sum'] or 0
        mst2 = Marks.objects.filter(student=student, exam_type="MST2").aggregate(Sum('marks'))['marks__sum'] or 0
        final = Marks.objects.filter(student=student, exam_type="FINAL").aggregate(Sum('marks'))['marks__sum'] or 0

        total = mst1 + mst2 + final

        results.append({
            "name": student.name,
            "mst1": mst1,
            "mst2": mst2,
            "final": final,
            "total": total
        })

    # Ranking
    results = sorted(results, key=lambda x: x['total'], reverse=True)

    for i, r in enumerate(results):
        r['rank'] = i + 1

    names = [r['name'] for r in results]
    totals = [r['total'] for r in results]

    context = {
        "results": results,
        "names": names,
        "totals": totals
    }

    return render(request,"result_dashboard.html",context)


def signup(request):

    form = StudentSignupForm()

    if request.method == "POST":

        form = StudentSignupForm(request.POST)

        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.warning(request,"Username already exists")
            return redirect("signup")

        if form.is_valid():

            user = User.objects.create_user(
                username=username,
                password=password
            )

            student = form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request,"Account created successfully")

            return redirect("login")

    return render(request,"signup.html",{"form":form})

# from .models import UserProfile


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            if role == "teacher":

                if Teacher.objects.filter(user=user).exists():
                    return redirect("admin_dashboard")

                else:
                    messages.error(request,"You are not registered as teacher")
                    return redirect("login")

            elif role == "student":

                if Student.objects.filter(user=user).exists():
                    return redirect("student_dashboard")

                else:
                    messages.error(request,"You are not registered as student")
                    return redirect("login")

        else:
            messages.error(request,"Invalid username or password")

    return render(request,"login.html")

def teacher_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user is not None:

            if Teacher.objects.filter(user=user).exists():

                login(request,user)

                return redirect("admin_dashboard")

        return render(request,"teacher_login.html",{
            "error":"Invalid teacher credentials"
        })

    return render(request,"teacher_login.html")

@login_required
def student_attendance(request):

    student = Student.objects.get(user=request.user)

    records = Attendance.objects.filter(student=student)

    return render(request,"student_attendance.html",{"records":records})

@login_required
def student_marks(request):

    student = Student.objects.get(user=request.user)

    marks = Marks.objects.filter(student=student)

    return render(request,"student_marks.html",{"marks":marks})

@login_required
def student_results(request):

    student = Student.objects.get(user=request.user)

    marks = Marks.objects.filter(student=student)

    return render(request,"student_results.html",{"marks":marks})


from django.db.models import Avg

@login_required
def student_marks(request):

    student = Student.objects.get(user=request.user)

    marks = Marks.objects.filter(student=student)

    # Subject-wise average marks
    subject_marks = Marks.objects.filter(student=student)\
        .values('subject__subject_name')\
        .annotate(avg_marks=Avg('marks'))

    subjects = []
    averages = []

    for s in subject_marks:
        subjects.append(s['subject__subject_name'])
        averages.append(round(s['avg_marks'],2))

    context = {
        "marks": marks,
        "subjects": subjects,
        "averages": averages
    }

    return render(request,"student_marks.html",{
    "marks": marks,
    "subjects": subjects,
    "averages": averages
})


import random
import time
from django.core.mail import send_mail

def forgot_password(request):

    if request.method == "POST":

        username = request.POST.get("username")
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")

        if "send_otp" in request.POST:
            try:
                user = User.objects.get(username=username)

                print("User email:", user.email)

                generated_otp = str(random.randint(1000, 9999))
                request.session['reset_otp'] = generated_otp
                request.session['reset_user'] = username
                request.session['otp_time'] = time.time()

                print("Sending OTP:", generated_otp)

                send_mail(
                    'Your OTP for Password Reset',
                    f'Your OTP is {generated_otp}',
                    'suryapaul9630@gmail.com',
                    [user.email],
                    fail_silently=False,
                )

                messages.success(request, "OTP sent to your email")

            except User.DoesNotExist:
                messages.error(request, "User not found")

        elif "reset_password" in request.POST:

            session_otp = request.session.get('reset_otp')
            session_user = request.session.get('reset_user')
            otp_time = request.session.get('otp_time')

            if otp_time and time.time() - otp_time > 300:
                messages.error(request, "OTP expired")
                return redirect("forgot_password")

            if otp == session_otp and username == session_user:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()

                request.session.flush()  # clear session

                messages.success(request, "Password reset successful")
                return redirect("login")
            else:
                messages.error(request, "Invalid OTP")

            return render(request, "forgot_password.html")

    if request.method == "POST":

        username = request.POST.get("username")
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")

        # STEP 1: Send OTP
        if "send_otp" in request.POST:
            try:
                user = User.objects.get(username=username)

                generated_otp = str(random.randint(1000, 9999))
                request.session['reset_otp'] = generated_otp
                request.session['reset_user'] = username
                request.session['otp_time'] = time.time()

                send_mail(
                    'Your OTP for Password Reset',
                    f'Your OTP is {generated_otp}',
                    'suryapaul9630@gmail.com',
                    [user.email],
                    fail_silently=False,
                )

                messages.success(request, "OTP sent to your email")

            except User.DoesNotExist:
                messages.error(request, "User not found")

        # STEP 2: Verify OTP & Reset Password
        elif "reset_password" in request.POST:

            session_otp = request.session.get('reset_otp')
            session_user = request.session.get('reset_user')
            otp_time = request.session.get('otp_time')
            # clr =request.session.flush('clr')

            if otp_time and time.time() - otp_time > 300:
                messages.error(request, "OTP expired. Please request a new one.")
                return redirect("forgot_password")

            if otp == session_otp and username == session_user:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()

                messages.success(request, "Password reset successful")
                return redirect("login")
            else:
                messages.error(request, "Invalid OTP")

    return render(request, "forgot_password.html")