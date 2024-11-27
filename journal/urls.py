from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("students/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("students/add", views.StudentCreateView.as_view(), name="student_add"),
    path("students/<int:pk>/edit/", views.StudentEditView.as_view(), name="student_edit"),
    path("students/<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student_delete"),
    path("teachers/", views.TeacherListView.as_view(), name="teacher_list"),
    path("teachers/<int:pk>/", views.TeacherDetailView.as_view(), name="teacher_detail"),
    path("teachers/add", views.TeacherCreateView.as_view(), name="teacher_add"),
    path("teachers/<int:pk>/edit/", views.TeacherEditView.as_view(), name="teacher_edit"),
    path("teachers/<int:pk>/delete/", views.TeacherDeleteView.as_view(), name="teacher_delete"),
    path("classes/", views.StudentClassDetailView.as_view(), name="class_list"),
    path("students/<int:pk>/grade/", views.GradeCreateView.as_view(), name="grade_add"),
    path("students/<int:pk>/grade/<int:grade_id>/", views.GradeEditView.as_view(), name="grade_edit"),
    path("grade/<int:grade_id>/", views.grade_delete, name="grade_delete"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='index'), name="logout"),
    path("", views.IndexView.as_view(), name="index"),
]