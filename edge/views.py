from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # image_url = <connection to server to get NCAP images>. Local for now.
    image_list = [("edge/CAP_DOS_2_CAR_0024__0081.jpg","im1"), ("edge/CAP_DOS_2_CAR_0024__0082.jpg", "im2")]
    context = {
        'image_list': image_list,
    }
    return render(request, 'edge/index.html', context)

def save(request):
    # image_url = <connection to server to get NCAP images>. Local for now.
    image_list = [("edge/CAP_DOS_2_CAR_0024__0081.jpg","im1"), ("edge/CAP_DOS_2_CAR_0024__0082.jpg", "im2")]
    context = {
        'image_list': image_list,
    }
    return render(request, 'edge/index.html', context)