from django.http import JsonResponse,HttpResponse
#from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from .forms import StudentForm
from .models import *
from django.contrib import messages
from django.db.models.functions import Length
from django.contrib.auth import authenticate,login
from django.contrib.auth import login as ln
# from  django.db.models import Value, CharField
from django.views.decorators.csrf import csrf_exempt
import uuid 
from django.conf import settings 
from django.core.mail import send_mail

def signup(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'User is already registered')
                return redirect('/')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is already registered')
                return redirect('/')

            user_obj= User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            send_mail_after_registration(email,auth_token)
            return redirect('token')
            return render(request,'core/login.html')
        except Exception as e:
            print(e)
    return render(request,'core/register.html')

def login(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        #email= request.POST.get('email')
        password= request.POST.get('pass')
        user=authenticate(username = username,password=password)
        # print(user)
        if user is not None:
            ln(request,user)
            return redirect('/home')
        else:
            messages.error(request, 'your password is incorrect..Please enter correctly')
    return render(request,'core/login.html')


def home(request):
    form = StudentForm()
    stu = Student.objects.all()
    context = {'form':form, 'stu':stu}
    return render(request, 'core/home.html', context)


@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            sid = request.POST.get('stuid')
            name = request.POST['name']
            #name.title()    
            #print(name)
            email = request.POST['email']
            course = request.POST['course']
            #print('student id',sid)

            if(sid == ''):
                s = Student(name=name, email=email, course=course)
            else:
                s = Student(id=sid, name=name, email=email, course=course)
            s.save()  
            # Student.objects.annotate(
            # name=Value(('name'), output_field=CharField()).capitalize()
# )    
            stu = Student.objects.values().order_by(Length('name')).order_by('name')
            #stu = Student.objects.values().order_by(Length('name'))
            # stu = Student.objects.all().update(name='capitalize')
            # stu.name = stu.name[0].capitalize() + stu.name[1:]
            # stu.save()
            #len = Student.objects.values_list('name', flat=True)
            #for i in len:
             #print(i)
            #student_data1 = list(i)
            student_data = list(stu)
            #print(type(student_data1))
            #len(student_data1)
            #for t in student_data1:
              # print(t)
            #print(len(student_data1))
            #print(i)
            return JsonResponse({'status':'Data Saved', 'student_data':student_data})
        else:
            return JsonResponse({'status':'Not Saved'})    

@csrf_exempt
def delete_data(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        s = Student.objects.get(pk=id)
        s.delete()  
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})    


@csrf_exempt
def edit_data(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        print('Student ID',id)
        student = Student.objects.get(pk=id)
        student_data = {'id':student.id, 'name':student.name, 'email':student.email, 'course':student.course}
        return JsonResponse(student_data)


# function for send mail

@csrf_exempt
def send_mail_after_registration(email):
   subject = 'Your  account need to verify...'
   messages = f'Hi!click the link to verify your account http://127.0.0.1:8000/home/'
   email_from = settings.EMAIL_HOST_USER 
   recipient_list = [email]
   send_mail(subject,messages ,email_from,recipient_list)















