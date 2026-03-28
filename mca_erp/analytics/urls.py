from django.urls import path
from . import views


urlpatterns = [

path('', views.home, name='home'),

# path('student/<int:id>/', views.student_dashboard, name='student_dashboard'),

path("student-dashboard/",views.student_dashboard,name="student_dashboard"),

path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

path('students/', views.student_list, name='student_list'),

path('add-student/', views.add_student, name='add_student'),

path('edit-student/<int:id>/', views.edit_student, name='edit_student'),

path('delete-student/<int:id>/', views.delete_student, name='delete_student'),

path('add-marks/',views.add_marks,name='add_marks'),

path('marks-dashboard/',views.marks_dashboard,name='marks_dashboard'),

path('mark-attendance/',views.mark_attendance,name='mark_attendance'),

path('attendance-history/', views.attendance_history, name='attendance_history'),

path('results/', views.result_dashboard, name='result_dashboard'),

path("signup/",views.signup,name="signup"),

path("login/", views.login_view, name="login"),

path("teacher-login/",views.teacher_login,name="teacher_login"),

path("student-dashboard/",views.student_dashboard,name="student_dashboard"),

path("my-attendance/",views.student_attendance,name="student_attendance"),

path("my-marks/",views.student_marks,name="student_marks"),

path("my-results/",views.student_results,name="student_results"),

path("forgot-password/", views.forgot_password, name="forgot_password"),

]