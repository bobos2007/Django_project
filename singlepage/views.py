from django.shortcuts import render

def landing(request):
    return render(
        request,
        'singlepage/landing.html',


    )

def about_me(request):
    return render(
        request,
        'singlepage/about_me.html',


    )