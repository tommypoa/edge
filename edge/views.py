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

im1_path = "edge/CAP_DOS_2_CAR_0024__0081.jpg"
im1_path = "edge/NCAP/Dominica/NCAP_DOS_3_DO_0001_0032.jpg"
im2_path = "edge/CAP_DOS_2_CAR_0024__0082.jpg"
visualization_output_path = "edge/static/edge/last_visualization.jpg"
point_format_path = "edge/world/df_format.points"

def index(request):
    # image_url = <connection to server to get NCAP images>. Local for now.
    image_list = [(im1_path, "im1"), (im2_path, "im2")]
    context = {
        'image_list': image_list,
    }
    return render(request, 'edge/index.html', context)

def save(request):
    im1_name = request.POST.get('im1_name')
    im2_name = request.POST.get('im2_name')
    length = request.POST.get('numPoints')

    for pointNum in range(int(length)):
        pt = request.POST.getlist('points[' + str(pointNum) + '][]')
        Coordinate.objects.create(
            im1_name = im1_name,
            im2_name = im2_name,
            im1_x = pt[0],
            im1_y = pt[1],
            im2_x = pt[2],
            im2_y = pt[3],
            created_at = timezone.now()
        )
    return JsonResponse({})

def visualize(request):
    df = pd.read_csv(point_format_path)

    length = request.POST.get('numPoints')
    for pointNum in range(int(length)):
        pt = request.POST.getlist('points[' + str(pointNum) + '][]')
        df = df.append(pd.Series(pt, index=df.columns), ignore_index=True)
    im1 = df.loc[:, ['mapX', 'mapY']].values
    im2 = df.loc[:, ['pixelX', 'pixelY']].values

    trans, _ = cv.estimateAffinePartial2D(
        np.float32(im2), np.float32(im1),
        method=cv.LMEDS)

    img1_file = "edge/static/" + im1_path
    img2_file = "edge/static/" + im2_path
    img1 = cv.imread(img1_file, cv.IMREAD_GRAYSCALE)
    img2 = cv.imread(img2_file, cv.IMREAD_GRAYSCALE)

    # fit img1 onto img0
    img_overlay = cv.warpAffine(src=img2, M=trans, dsize=img1.shape[::-1])
    # overlay with 50% transparency
    img_overlay = cv.addWeighted(img1, 0.5, img_overlay, 0.5, gamma=0.0)
    output_url = visualization_output_path
    cv.imwrite(output_url, img_overlay)
    response_data = {'url': output_url[4:]}
    return JsonResponse(response_data)