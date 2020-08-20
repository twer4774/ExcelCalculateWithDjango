from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import *

# Create your views here.
def index(request):
    return render(request,'main/index.html')

def signup(request):
    return render(request, 'main/signup.html')

def join(request):
    print(request)
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
    user.save()

    #인증코드 만들기 - 4자리
    code = randint(1000, 9999)
    response = redirect('main_verifyCode')
    #쿠키에 인증코드 저장
    response.set_cookie('code', code)
    #어떤 유저를 인증하는지 알기 위해 user_id를 쿠키에 저장
    response.set_cookie('user_id', user.id)

    #이메일 발송 함수 호출
    send_result = send(email, code)
    if send_result:
        return response
    else:
        return HttpResponse("이메일 발송에 실패했습니다.")
    #인증 코드 입력화면으로 이동
    return response

def signin(request):
    return render(request, 'main/signin.html')

def verifyCode(request):
    return render(request, 'main/verifyCode.html')

def verify(request):
    user_code = request.POST['verifyCode']
    cookie_code = request.COOKIES.get('code')
    if user_code == cookie_code:
        user = User.objects.get(id = request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('main_index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        response.set_cookie('user',user)
        return response
    else:
        return redirect('main_index')

def result(request):
    return render(request, 'main/result.html')