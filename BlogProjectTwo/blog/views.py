from django.shortcuts import render,redirect,get_object_or_404
from blog.forms import SignUpForm,CommentForm,EmailSendForm,PostForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from blog.models import Post
from taggit.models import Tag
from django.core.mail import send_mail
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


# Create your views here.

def index(request):
    return render(request,'blog/base.html')

def sign_up_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        user = form.save()
        user.set_password(user.password)
        user.save()
        return redirect('index')
    return render(request,'blog/signup.html',locals())

def post_list_view(request,tag_slug=None):
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in = [tag])
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'blog/post_list.html',locals())


def post_detail_view(request,year,month,day,post):
    post = get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)
    csubmit = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit = False)
            new_comment.post = post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()
    return render(request,'blog/post_detail.html',locals())


@login_required
def mail_send_view(request,id):
    post = get_object_or_404(Post,id=id,status='published')
    sent = False
    if request.method == 'POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = '{}({}) recommended you to read "{}"'.format(cd['name'],cd['email'],post.title)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message = 'Read post at:\n\n{}\n\n{}\'s Comments :\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'akash@blog.com',[cd['to']])
            sent = True
    else:
        form = EmailSendForm()
    return render(request,'blog/sharebymail.html',locals())

@login_required
def add_post_view(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('base')
            print(form.cleaned_data)
    return render(request,'blog/form.html',locals())

def post_list_full_view(request,tag_slug=None):
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in = [tag])
    paginator = Paginator(post_list,3)
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request,'blog/post_list_full.html',locals())


import re
from django.db.models import Q

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

def search_post(request):
    query_string = ''
    found_queries = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string,['title','body',])
        print(entry_query)
        post_list = Post.objects.filter(entry_query)

        return render(request,'blog/post_list_full.html',locals())
