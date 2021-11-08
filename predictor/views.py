from django.shortcuts import render

# Create your views here.

def predictor_main(request):
    return render(request,'predictor/predictor_main.html')