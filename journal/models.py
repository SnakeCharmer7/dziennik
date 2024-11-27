from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    head_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="classes")
    name = models.CharField(max_length=20)
    form_tutor = models.OneToOneField(Teacher, on_delete=models.SET_NULL, null=True, related_name='student_class_tutor')

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='students')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Subject(models.Model):
    name = models.CharField(max_length=50)
    main_teacher = models.OneToOneField(Teacher, on_delete=models.SET_NULL, null=True, related_name="subject")

    def __str__(self):
        return f"{self.name}"


class Grade(models.Model):
    MARKS = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    mark = models.IntegerField(choices=MARKS)
    date = models.DateTimeField(auto_now_add=True)