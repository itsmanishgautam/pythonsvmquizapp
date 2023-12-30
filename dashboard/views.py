from django.shortcuts import render,HttpResponse,redirect
from questionapp.models import Question,Test
from questionapp.forms import QuestionForm,AnswerForm,TestForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout,password_validation
from django.core.exceptions import ValidationError

from .forms import UserRegistrationForm
# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required()
def home(request):
    # return HttpResponse("OK")
    context = {

    }
    return render(request,'dashboard/dashboard.html',context)

@login_required()
def testPage(request,test_id):
    context = {
        'test_id':test_id
    }
    return render(request,'dashboard/testpage.html',context)


@login_required()
def logoutPage(request):
    logout(request)
    messages.info(request,"Logout Successfully")
    return redirect('dashboard:login')


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard:home')
        else:
            messages.info(request,"Username or Password Incorrect")
 
    context ={}
    return render(request,'login.html',context)

def signupPage(request):
    if request.method == 'POST':
        first_name  = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        form  = UserRegistrationForm(request.POST)
        # if form.is_vaild():
        if first_name is not None and last_name is not None and username is not None and password is not None :
            if not User.objects.filter(username__iexact=username).exists():
                if password:
                    try:
                        password_validation.validate_password(password, User)
                    except ValidationError as error:
                        messages.info(request,f'{error}')
                user = User.objects.create(username=username,first_name=first_name,last_name=last_name)
                user.set_password(password)
                user.save()

            else:
                messages.info(request,f'username {username} already taken')
            messages.info(request,"User Registered")
            return redirect('dashboard:login')
        else:
            messages.info('Please correct errors!')


    context = {}
    return render(request,'signup.html',context)

@login_required()
def list_questions(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:questionpool')

    questions = Question.objects.all().prefetch_related('answers')
    context = {
        'questions':questions,
        'form':form
    }

    return render(request,'dashboard/list_questions.html',context)

@login_required()
def add_option(request,question_id):
    form  = AnswerForm()
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = question_id
            answer.save()
            return redirect('dashboard:questionpool')
    question = Question.objects.get(id=question_id)
    context = {
        'question':question,
        'form':form
    } 

    return render(request,'dashboard/add_option.html',context)

@login_required()    
def list_test(request):
    tests = Test.objects.all()
    form = TestForm()
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect('dashboard:list_test')
        
    context = {
        'tests':tests,
        'form':form
    }
    return render(request,'dashboard/list_test.html',context)


@login_required()
def add_test(request):
    form = TestForm()
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect('dashboard:add_test')
        
    context = {
        'form':form
    }
    return render(request,'dashboard/add_test.html',context)


@login_required()
def test_index(request):
    tests = Test.objects.all()
    context = {
        'tests':tests
    }
    return render(request,'dashboard/take_test_index.html',context)