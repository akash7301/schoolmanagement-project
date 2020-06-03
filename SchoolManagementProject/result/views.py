from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from corecode.models import AcademicSession,AcademicTerm
from students.models import Student

from .models import Result
from .forms import CreateResult,EditResult
# Create your views here.

@login_required
def create_result(request):
    students = Student.objects.all()
    if request.method == 'POST':
        if 'finish' in request.POST:
            form = CreateResult(request.POST)
            if form.is_valid():
                subjects = form.cleaned_data['subjects']
                session = form.cleaned_data['session']
                term = form.cleaned_data['term']
                students = request.POST['students']
                results = []
                for student in students.split(','):
                    stu = Student.objects.get(pk=student)
                    for subject in subjects:
                        check = Result.objects.filter(session=session,term=term,current_class=stu.current_class,subject=subject,student=stu).first()
                        if not check:
                            results.append(Result(session=session,
                                                  term=term,
                                                  current_class=stu.current_class,
                                                  subject=subject,
                                                  student=stu))
                Result.objects.bulk_create(results)
                return redirect('edit-results')

        id_list = request.POST.getlist('students')
        if id_list:
            form = CreateResult(initial={'session':request.current_session,'term':request.current_term})
            studentlist = ','.join(id_list)
            return render(request,'result/create_result_page2.html',{'students':studentlist,'form':form,'count':len(id_list)})
        else:
            messages.warning(request,"You didn't select any student.")
    return render(request,'result/create_result.html',{'students':students})

@login_required
def edit_result(request):
    if request.method == 'POST':
        form = EditResult(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Result successfully updated')
            return redirect('view-results')
    else:
        results = Result.objects.filter(session=request.current_session,term=request.current_term)
        form = EditResult(queryset=results)
    return render(request,'result/edit_result.html',{'formset':form})

@login_required
def all_results_view(request):
    results = Result.objects.filter(session=request.current_session,term=request.current_term)

    bulk = {}
    for result in results:
        test_total = 0
        exam_total = 0
        subjects = []
        for subject in results:
            if subject.student == result.student:
                subjects.append(subject)
                test_total += subject.test_score
                exam_total += subject.exam_score

        bulk[result.student.id] = {
            'student':result.student,
            'subjects':subjects,
            'test_total':test_total,
            'exam_total':exam_total,
            'total_total':test_total+exam_total
        }

    context = {'results':bulk}

    return render(request,'result/all_results.html',context)
