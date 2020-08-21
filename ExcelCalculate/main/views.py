from django.shortcuts import render, redirect
from random import *
from .models import *
from sendEmail.views import *

# Create your views here.
#세션에 저장된 정보로 로그인된 사용자를 확인. 로그인이 안되어 있다면 로그인화면으로 이동
def index(request):
    if 'user_name' in request.session.keys():
        return render(request, 'main/index.html')
    else:
        return redirect('main_signin')

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

def login(request):
    loginEmail = request.POST['loginEmail']
    loginPW = request.POST['loginPW']
    user = User.objects.get(user_eamil = loginEmail)
    if user.user_paswword == loginPW:
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return redirect('main_index')
    else:
        return redirect('main_loginFail')

def logout(request):
    del request.session['user_name']
    del request.session['user_email']
    return redirect('main_signin')

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
        # response.set_cookie('user',user)
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return response
    else:
        return redirect('main_verifyCode')

def result(request):
   if 'user_name' in request.session.keys():
        return render(request, 'main/result.html')
   else:
        return redirect('main_signin')