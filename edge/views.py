from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Coordinate
import logging
from django.http import JsonResponse


def index(request):
    # image_url = <connection to server to get NCAP images>. Local for now.
    image_list = [("edge/CAP_DOS_2_CAR_0024__0081.jpg","im1"), ("edge/CAP_DOS_2_CAR_0024__0082.jpg", "im2")]
    context = {
        'image_list': image_list,
    }
    return render(request, 'edge/index.html', context)

def save(request):
    response_data = {}

    if request.is_ajax():
        im1_name = request.POST.get('im1_name')
        im2_name = request.POST.get('im2_name')
        im1_x = request.POST.get('im1_x')
        im1_y = request.POST.get('im1_y')
        im2_x = request.POST.get('im2_x')
        im2_y = request.POST.get('im2_y')
        
        response_data['im1_name'] = im1_name
        response_data['im2_name'] = im2_name
        response_data['im1_x'] = im1_x
        response_data['im1_y'] = im1_y
        response_data['im2_x'] = im2_x
        response_data['im2_y'] = im2_y

        Coordinate.objects.create(
            im1_name = im1_name,
            im2_name = im2_name,
            im1_x = im1_x,
            im1_y = im1_y,
            im2_x = im2_x,
            im2_y = im2_y,
            created_at = timezone.now()
        )
        return JsonResponse(response_data)
    else:
        return HttpResponseRedirect(reverse('edge:index'))