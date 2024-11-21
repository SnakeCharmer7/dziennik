from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Teacher, Student, StudentClass, School, Subject, Grade
from django.urls import reverse_lazy
from .forms import TeacherForm


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
    fields = ['first_name', 'last_name', 'email', 'student_class']
    template_name = "journal/form.html"
    success_url = reverse_lazy('student_list')


class StudentDeleteView(generic.DeleteView):
    model = Student
    template_name = "journal/student_confirm_delete.html"
    success_url = reverse_lazy('student_list')


class StudentCreateView(generic.CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'email', 'student_class']
    template_name = "journal/form.html"
    success_url = reverse_lazy('student_list')


class GradeCreateView(generic.CreateView):
    model = Grade
    fields = ['subject', 'mark']
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
    fields = ['mark']
    template_name = 'journal/grade_edit.html'

    def get_object(self, queryset=None):
        grade_id = self.kwargs.get('grade_id')
        return get_object_or_404(Grade, pk=grade_id)

    def get_success_url(self):
        student = self.object.student
        return reverse_lazy('student_detail', kwargs={'pk': student.pk})


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
    template_name = "journal/form.html"
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
    template_name = "journal/form.html"
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