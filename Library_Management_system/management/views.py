from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import datetime,random

# Create your views here.
#Home page
def index(request):
    return render(request,'index.html')

#view that  will return list of all book in library
def BookListView(request):
    book_list = Book.objects.all()
    return render(request,'catalog/book_list.html',locals())

@login_required
def student_BookListView(request):
    student = Student.objects.get(roll_no=request.user)
    bor = Borrower.objects.filter(student=student)
    book_list = []
    for b in bor:
        book_list.append(b.book)

    return render(request,'catalog/book_list.html',locals())

def BookDetailView(request,pk):
    book = get_object_or_404(Book,id=pk)
    reviews = Reviews.objects.filter(book=book).exclude(review='none')
    try:
        stu = Student.objects.get(roll_no=request.user)
        rr = Reviews.objects.get(review='none')
    except:
        pass
    return render(request,'catalog/book_detail.html',locals())


@login_required
def BookCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request,'catalog/form.html',locals())

@login_required
def BookUpdate(request,pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Book.objects.get(id=pk)
    form = BookForm(instance=obj)
    if request.method == 'POST':
        form = BookForm(data=request.POST,files=request.FILES,instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('index')
    return render(request,'catalog/form.html',locals())

@login_required
def BookDelete(request,pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = get_object_or_404(Book,pk=pk)
    obj.delete()
    return redirect('index')


@login_required
def student_request_issue(request, pk):
    obj = Book.objects.get(id=pk)
    stu=Student.objects.get(roll_no=request.user)
    s = get_object_or_404(Student, roll_no=str(request.user))
    if s.total_book_due < 10:
        message = "Book has been isuued, You can collect book from library"
        a = Borrower()
        a.student = s
        a.book = obj
        a.issue_date = datetime.datetime.now()
        obj.available_copies = obj.available_copies - 1
        obj.save()
        stu.total_book_due=stu.total_book_due+1
        stu.save()
        a.save()
        rand1 = random.choice('0123456789')
        rand2 = random.choice('0123456789')
        rand3 = random.choice('0123456789')
        rand4 = random.choice('0123456789')
        tokan = rand1 + rand2 + rand3 + rand4
    else:
        message = "you have exceeded limit."
    return render(request, 'catalog/result.html', locals())

@login_required
def StudentCreate(request):
    if not request.user.is_superuser:
        return redirect('index')
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            n = form.cleaned_data['name']
            e = form.cleaned_data['email']
            username = (str(n.split(' ')[0])).lower()
            r = str(form.cleaned_data['roll_no'])
            pas = username+str(r[8:])
            pas = pas.lower()
            print(username,'***************',pas,'*************')
            u = User.objects.get(username=r)
            u.email = e
            u.set_password(pas)
            u.save()
            return redirect('index')
    return render(request,'catalog/form.html',locals())

@login_required
def StudentUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Student.objects.get(id=pk)
    form = StudentForm(instance=obj)
    if request.method == 'POST':
        form = StudentForm(data=request.POST,files=request.FILES,instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj.save()
            return redirect('index')
    return render(request,'catalog/form.html',locals())


@login_required
def StudentDelete(request,pk):
    obj = get_object_or_404(Student,pk=pk)
    roll_no = obj.roll_no
    user = User.objects.get(username=roll_no)
    user.delete()
    obj.delete()
    return redirect('index')

@login_required
def StudentList(request):
    students = Student.objects.all()
    return render(request,'catalog/student_list.html',locals())

@login_required
def StudentDetail(request,pk):
    student = get_object_or_404(Student, id=pk)
    books = Borrower.objects.filter(student=student)
    return render(request,'catalog/student_detail.html',locals())


login_required
def ret(request,pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = Borrower.objects.get(id=pk)
    book_pk = obj.book.id
    student_pk = obj.student.id
    student = Student.objects.get(id=student_pk)
    student.total_book_due -= 1
    student.save()

    book = Book.objects.get(id=book_pk)
    rating = Reviews(review='none',book=book,student=student,rating='2.5')
    rating.save()
    obj.delete()
    return redirect('index')


import re
from django.db.models import Q

# def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S)').findall, normspace=re.compile(r'\s{2,}').sub):
#     return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def normalize_query(query_string):
    s = query_string.split(' ')
    return s


def get_query(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query


def search_book(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string,['title','summary','auther'])
        
        book_list = Book.objects.filter(entry_query)

        return render(request,'catalog/book_list.html',locals())

def search_student(request):
    query_string = ''
    found_entries = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['roll_no','name','email'])

        students = Student.objects.filter(entry_query)

        return render(request,'catalog/student_list.html',locals())

@login_required
def RatingUpdate(request, pk):
    obj = Reviews.objects.get(id=pk)
    form = RatingForm(instance=obj)
    if request.method=='POST':
        form = RatingForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.save()
            return redirect('book-detail', pk=obj.book.id)
    return render(request,'catalog/form.html',locals())

@login_required
def RatingDelete(request, pk):
    obj = get_object_or_404(Review, pk=pk)
    st = Student.objects.get(roll_no=request.user)
    if not st==obj.student:
        return redirect('index')
    pk = obj.book.id
    obj.delete()
    return redirect('book-detail',pk)
