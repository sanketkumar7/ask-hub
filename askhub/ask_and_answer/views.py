from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import make_password
from .models import User,Question,Answer,Like
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated
from django.template.loader import render_to_string
from .forms import user_form,question_form
# Create your views here.

def home_page(req):
    form=question_form(initial={'author':req.user.username})
    questions=Question.objects.all().values().order_by('-id')
    for que in questions:
        answer_ls=[]
        answers=Answer.objects.filter(question=que['id']).values()
        for ans in answers: 
            ans['like']=Like.objects.filter(answer=ans['id'],user=req.user).exists()
            answer_ls.append(ans)
            answer_ls.sort(key=lambda x: x['likes'], reverse=True)
        que['answers']=answer_ls
    if req.method=='POST':
        if not req.user.is_authenticated:
            messages.error(req,'Please login into your account.')
            return redirect('login_user')
        
        form=question_form(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req,'Question is added successfully.')
            return redirect('home')
    context={
        'form':form,
        'questions':questions
    }
    return render(req,'aaa/home.html',context)

@unauthenticated
def login_user(req):
    if req.method=="POST":
        username=req.POST['username']
        password=req.POST['password']
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            user=None
        if user and user.check_password(password):
            login(req,user)
            messages.success(req,f'Welcome {user.username}.')
            return redirect('home')
        else:
            messages.error(req,'Invalid Username or Password.')
    return render(req,'aaa/login.html')

@unauthenticated
def register_user(req):
    form= user_form()
    if req.method=="POST":
        form=user_form(req.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.password=make_password(user.password)
            user.save()
            messages.success(req,f'{user.username} Registered. Please Log in.')
            return redirect('login_user')
    context={
        'form':form
    }
    return render(req,'aaa/registration.html',context)

def logout_user(req):
    logout(req)
    messages.success(req,'Successfully logout. Please log in.')
    return redirect('login_user')

@login_required(login_url='login_user')
def post_answer(req,id):
    question=Question.objects.get(id=id)
    answers=Answer.objects.filter(question=question).values()
    if req.method=="POST":
        ans=req.POST['answer']
        Answer.objects.create(question=question,author=req.user.username,answer=ans)
        messages.success(req,'You answer posted successfully.')
        return redirect('home')
    context={
        'question':question,

    }
    return render(req,'aaa/post_answer.html',context)

@login_required(login_url='login_user')
def user_questions(req):
    questions=Question.objects.filter(author=req.user.username).values().order_by('-id')
    for que in questions:
        answer_ls=[]
        answers=Answer.objects.filter(question=que['id']).values()
        for ans in answers: 
            ans['like']=Like.objects.filter(answer=ans['id'],user=req.user).exists()
            answer_ls.append(ans)
            answer_ls.sort(key=lambda x: x['likes'], reverse=True)
        que['answers']=answer_ls
    return render(req,'aaa/user_questions.html',{'questions':questions})

@login_required(login_url='login_user')
def delete_question(req,id):
    question=Question.objects.get(id=id)
    question.delete()
    messages.warning(req,'Question is deleted successfully.')
    return redirect('user_questions')
# Ajax requests

@login_required(login_url='login_user')
def like_unlike(req,id):
    answer=Answer.objects.get(id=id)
    try:
        like=Like.objects.get(answer=answer,user=req.user)
        answer.likes-=1
        like.delete()
    except Like.DoesNotExist:
        Like.objects.create(answer=answer,user=req.user)
        answer.likes+=1
    finally:
        answer.save()
    questions=Question.objects.all().values().order_by('-id')
    for que in questions:
        answer_ls=[]
        answers=Answer.objects.filter(question=que['id']).values()
        for ans in answers: 
            ans['like']=Like.objects.filter(answer=ans['id'],user=req.user).exists()
            answer_ls.append(ans)
            answer_ls.sort(key=lambda x: x['likes'], reverse=True)
        que['answers']=answer_ls
        dbody_html = render_to_string('aaa/ajax/dbody.html', {'questions': questions})
    return JsonResponse({'updated':True,'dbody_html':dbody_html})
