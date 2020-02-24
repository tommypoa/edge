from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Coordinate
import logging
from django.http import JsonResponse
import cv2 as cv
import pandas as pd
from PIL import Image
import numpy as np


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

def visualize(request):
    logger = logging.getLogger(__name__)
    file = 'edge/world/test.points'
    pts0 = request.POST.getlist('points[0][]')
    pts1 = request.POST.getlist('points[1][]')
    df = pd.read_csv(file)
    df = df.append(pd.Series(pts0, index=df.columns), ignore_index=True)
    df = df.append(pd.Series(pts1, index=df.columns), ignore_index=True)
    pts0 = df.loc[:, ['mapX', 'mapY']].values
    pts1 = df.loc[:, ['pixelX', 'pixelY']].values

    trans, _ = cv.estimateAffinePartial2D(
        np.float32(pts1), np.float32(pts0),
        method=cv.LMEDS)

    img0_file = 'edge/static/edge/CAP_DOS_2_CAR_0024__0081.jpg'
    img1_file = 'edge/static/edge/CAP_DOS_2_CAR_0024__0082.jpg'
    img0 = cv.imread(img0_file, cv.IMREAD_GRAYSCALE)
    img1 = cv.imread(img1_file, cv.IMREAD_GRAYSCALE)

    # fit img1 onto img0
    img_overlay = cv.warpAffine(src=img1, M=trans, dsize=img0.shape[::-1])
    # overlay with 50% transparency
    img_overlay = cv.addWeighted(img0, 0.5, img_overlay, 0.5, gamma=0.0)
    output_url = 'edge/static/edge/visualization.jpg'
    cv.imwrite(output_url, img_overlay)
    response_data = {'url': output_url[4:]}
    return JsonResponse(response_data)