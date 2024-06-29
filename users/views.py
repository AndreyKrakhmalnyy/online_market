from django.shortcuts import render



def login(request):
    
    context = {
        'login': 'Home - Авторизацмя',
    }
    return render(request, 'users/login.html', context)

def registration(request):

    context = {
        'registration': 'Home - Регистрация',
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    
    context = {
        'profile': 'Home - Личный кабинет',
    }
    return render(request, 'users/profile.html', context)

def logout(request):
    pass    
    # context = {
    #     'profile': 'Home - Личный кабинет',
    # }
    # return render(request, 'users/profile.html', context)