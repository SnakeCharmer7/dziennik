from django import forms
from .models import Teacher, Student, Subject, StudentClass

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'student_class']

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