from django import forms
from django.contrib.auth.models import User
from .models import Teacher, Student, Subject, StudentClass, Grade
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(label="Imię")
    last_name = forms.CharField(label="Nazwisko")
    profile_picture = forms.FileField(
        required=False,
        label="Zdjęcie profilowe",
        error_messages={'invalid': "Zdjęcie musi być w formacie JPG, JPEG lub PNG."}
    )
    email = forms.EmailField(label="Adres e-mail")

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'student_class', 'profile_picture']

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            try:
                img = Image.open(picture)
                img.verify()
                if img.format not in ['JPEG', 'JPG', 'PNG']:
                    raise forms.ValidationError("Zdjęcie musi być w formacie JPG, JPEG lub PNG")
            except Exception:
                raise forms.ValidationError("Przesłany plik nie jest obrazem.")
        return picture


class StudentCreateForm(StudentForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Uczeń z takim adresem email już istnieje.")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        student = super().save(commit=False)
        student.user = user
        
        if commit:
            student.save()
        return student
    

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email']

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        label="Przedmiot"
    )

    student_class = forms.ModelChoiceField(
        queryset=StudentClass.objects.all(),
        required=False,
        label="Klasa wychowawcza"
    )
    
    def clean_student_class(self):
        student_class = self.cleaned_data.get('student_class')
        if student_class and student_class.form_tutor and student_class.form_tutor != self.instance:
            raise forms.ValidationError("Ta klasa już ma przypisanego wychowawcę.")
        return student_class

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if subject:
            if subject.main_teacher and subject.main_teacher != self.instance:
                raise forms.ValidationError("Ten przedmiot ma już przypisanego nauczyciela.")
        return subject

    def save(self, commit=True):
        teacher = super().save(commit=False)

        student_class = self.cleaned_data.get('student_class')
        if student_class:
            student_class.form_tutor = teacher
            student_class.save()

        subject = self.cleaned_data.get('subject')
        if subject:
            subject.main_teacher = teacher
            subject.save()

        if commit:
            teacher.save()

        return teacher