from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Teacher, Student, StudentClass, School, Subject, Grade
from django.urls import reverse_lazy, reverse
from .forms import TeacherForm, StudentForm, StudentCreateForm, LoginForm, GradeEditForm, GradeAddForm
from django.contrib.auth.views import LoginView, LogoutView


class StudentListView(generic.ListView):
    model = Student
    template_name = "journal/student_list.html"
    context_object_name = "students"


class StudentDetailView(generic.DetailView):
    model = Student
    template_name = "journal/student_detail.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grades_by_subject = {}
        for grade in self.object.grades.all():
            if grade.subject.name not in grades_by_subject:
                grades_by_subject[grade.subject.name] = []
            grades_by_subject[grade.subject.name].append(grade)

        context['grades_by_subject'] = grades_by_subject
        return context


class StudentEditView(generic.UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "journal/student_edit_form.html"
    success_url = reverse_lazy('student_list')


class StudentDeleteView(generic.DeleteView):
    model = Student
    template_name = "journal/student_confirm_delete.html"
    success_url = reverse_lazy('student_list')

def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')


class StudentCreateView(generic.CreateView):
    model = Student
    form_class = StudentCreateForm
    template_name = "journal/student_add_form.html"
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        return super().form_valid(form)


class GradeCreateView(generic.CreateView):
    model = Grade
    form_class = GradeAddForm
    template_name = "journal/grade_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.student = get_object_or_404(Student, id=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.student = self.student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.student.id})


class GradeEditView(generic.UpdateView):
    model = Grade
    form_class = GradeEditForm
    template_name = 'journal/grade_edit.html'

    def get_object(self, queryset=None):
        grade_id = self.kwargs.get('grade_id')
        return get_object_or_404(Grade, pk=grade_id)

    def get_success_url(self):
        student = self.object.student
        return reverse_lazy('student_detail', kwargs={'pk': student.pk})


def grade_delete(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    student_id = grade.student.id
    grade.delete()
    return redirect(reverse('student_detail', kwargs={'pk': student_id}))


class TeacherListView(generic.ListView):
    model = Teacher
    template_name = "journal/teacher_list.html"
    context_object_name = "teachers"


class TeacherDetailView(generic.DetailView):
    model = Teacher
    template_name = "journal/teacher_detail.html"
    context_object_name = "teacher"


class TeacherCreateView(generic.CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "journal/teacher_add_form.html"
    success_url = reverse_lazy('teacher_list')

    def form_valid(self, form):
        subject = form.cleaned_data.get('subject')
        if subject:
            subject.main_teacher = self.object
            subject.save()

        return super().form_valid(form)


class TeacherEditView(generic.UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "journal/teacher_edit_form.html"
    success_url = reverse_lazy('teacher_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        teacher = self.get_object()

        subject = Subject.objects.filter(main_teacher=teacher).first()
        if subject:
            form.fields['subject'].initial = subject

        student_class = StudentClass.objects.filter(form_tutor=teacher).first()
        if student_class:
            form.fields['student_class'].initial = student_class

        return form

    def form_valid(self, form):
        subject = form.cleaned_data.get('subject')
        if subject:
            subject.main_teacher = self.object
            subject.save()
        else:
            Subject.objects.filter(main_teacher=self.object).update(main_teacher=None)

        new_class = form.cleaned_data.get('student_class')

        StudentClass.objects.filter(form_tutor=self.object).update(form_tutor=None)

        if new_class:
            self.object.form_tutor = self.object
            new_class.save()

        return super().form_valid(form)


class TeacherDeleteView(generic.DeleteView):
    model = Teacher
    template_name = "journal/teacher_confirm_delete.html"
    success_url = reverse_lazy('teacher_list')


class StudentClassDetailView(generic.ListView):
    model = StudentClass
    template_name = "journal/class_list.html"
    context_object_name = "classes"


class IndexView(generic.ListView):
    model = School
    template_name = 'journal/index.html'
    context_object_name = 'school'


class CustomLoginView(LoginView):
    template_name = 'journal/login.html'
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("student_list")
        else:
            return reverse_lazy('student_detail', kwargs={'pk': self.request.user.student.pk})
