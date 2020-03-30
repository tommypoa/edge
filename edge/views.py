from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Coordinate
from .models import ImPair
import logging
from django.http import JsonResponse
import cv2 as cv
import pandas as pd
from PIL import Image
import numpy as np
import csv
import logging

visualization_output_path = "edge/static/NCAP/last_visualization.jpg"
point_format_path = "edge/world/df_format.points"

def index(request):
    # image_url = <connection to server to get NCAP images>. Local for now.
    pair_id, im1_path, im2_path = get_next_pair()
    if pair_id == None:
        return render(request, 'edge/completed.html')
    image_list = [(im1_path, "im1"), (im2_path, "im2")]
    context = {
        'image_list': image_list,
        'pair_id': pair_id
    }
    return render(request, 'edge/index.html', context)

def save(request):
    im1_name = request.POST.get('im1_name')
    im2_name = request.POST.get('im2_name')
    pair_id = request.POST.get('pair_id')
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
        ImPair.objects.filter(pk=pair_id).update(linked=True)
    return JsonResponse({})

def visualize(request):
    df = pd.read_csv(point_format_path)

    length = request.POST.get('numPoints')
    im1_name = request.POST.get('im1_name')
    im2_name = request.POST.get('im2_name')

    for pointNum in range(int(length)):
        pt = request.POST.getlist('points[' + str(pointNum) + '][]')
        df = df.append(pd.Series(pt, index=df.columns), ignore_index=True)
    im1 = df.loc[:, ['mapX', 'mapY']].values
    im2 = df.loc[:, ['pixelX', 'pixelY']].values

    trans, _ = cv.estimateAffinePartial2D(
        np.float32(im2), np.float32(im1),
        method=cv.LMEDS)

    img1_file = "edge/static/" + im1_name
    img2_file = "edge/static/" + im2_name
    img1 = cv.imread(img1_file, cv.IMREAD_GRAYSCALE)
    img2 = cv.imread(img2_file, cv.IMREAD_GRAYSCALE)
    # fit img1 onto img0
    img_overlay = cv.warpAffine(src=img2, M=trans, dsize=img1.shape[::-1])
    # overlay with 50% transparency
    # img_overlay = cv.addWeighted(img1, 0.5, img_overlay, 0.5, gamma=0.0)
    output_url = visualization_output_path
    cv.imwrite(output_url, img_overlay)
    response_data = {'url': output_url[4:]}
    return JsonResponse(response_data)

### HELPER FUNCTIONS

def get_next_pair():
    unlinked_pairs = ImPair.objects.filter(linked=False)
    if unlinked_pairs.count() == 0:
        return [None, None, None]
    pair = unlinked_pairs[0]
    im1_name = "NCAP/" + pair.island + "/" + pair.collection_id + "_" + str(f'{pair.im1id0:04}') + "/" + \
        pair.collection_id + "_" + str(f'{pair.im1id0:04}') + "_" + str(f'{pair.im1id1:04}') + ".jpg"
    im2_name = "NCAP/" + pair.island + "/" + pair.collection_id + "_" + str(f'{pair.im2id0:04}') + "/" + \
        pair.collection_id + "_" + str(f'{pair.im2id0:04}') + "_" + str(f'{pair.im2id1:04}') + ".jpg"
    return [pair.id, im1_name, im2_name]


def create_links(request):
    with open("edge/static/links.csv") as f:
        reader = csv.reader(f)
        next(reader, None) # Skip the headers
        for row in reader:
            _, created = ImPair.objects.get_or_create(
                island=row[0],
                collection_id=row[2],
                im1id0 = row[3],
                im1id1 = row[4],
                im2id0 = row[5],
                im2id1 = row[6]
                )
    return redirect('edge:index')
