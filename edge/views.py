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
import os

visualization_output_path = "edge/static/NCAP/"
point_format_path = "edge/world/df_format.points"
resizeFactor = 10
islands = ["dominica", "montserrat", "caymanislands", "jamaica", "virginislands", "stvincentgrenadines", "stlucia"]

def select_island(request):
    island_completion_count = []
    for island in islands:
        current_set = ImPair.objects.filter(island=island)
        current_set_linked = current_set.filter(linked=True)
        island_completion_count.append([island, current_set_linked.count, current_set.count])
    context = {'island_counts': island_completion_count}
    return render(request, 'edge/select_island.html', context)

def index(request, island):
    # image_url = <connection to server to get NCAP images>. Local for now.
    pair_id, im1_path, im2_path = get_next_pair(island)
    if pair_id == None:
        context = {'island': island}
        return render(request, 'edge/completed.html', context)
    image_list = [(im1_path, "im1"), (im2_path, "im2")]
    context = {
        'image_list': image_list,
        'pair_id': pair_id,
        'island': island
    }
    return render(request, 'edge/index.html', context)

def save(request):
    im1_name = request.POST.get('im1_name')
    im2_name = request.POST.get('im2_name')
    pair_id = request.POST.get('pair_id')
    length = request.POST.get('numPoints')

    for pointNum in range(int(length)):
        pt = request.POST.getlist('points[' + str(pointNum) + '][]')
        pair = ImPair.objects.filter(pk=pair_id)
        Coordinate.objects.create(
            im1_name = im1_name,
            im2_name = im2_name,
            im1_x = str(float(pt[0]) * resizeFactor),
            im1_y = str(float(pt[1]) * resizeFactor),
            im2_x = str(float(pt[2]) * resizeFactor),
            im2_y = str(float(pt[3]) * resizeFactor),
            pair = pair.first(),
            created_at = timezone.now()
        )
        pair.update(linked=True)
    return JsonResponse({})

def visualize(request):
    df = pd.read_csv(point_format_path)

    length = request.POST.get('numPoints')
    im1_name = request.POST.get('im1_name')
    im2_name = request.POST.get('im2_name')
    island = request.POST.get('island')

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
    img_overlay = cv.addWeighted(img1, 0.5, img_overlay, 0.5, gamma=0.0)
    output_url = visualization_output_path + island + "_visualization.jpg"
    cv.imwrite(output_url, img_overlay)
    response_data = {'url': output_url[4:]}
    return JsonResponse(response_data)

def create_links(request):
    duplicate_links = []
    with open("edge/static/human_links_01232021.csv") as f:
        reader = csv.reader(f)
        next(reader, None) # Skip the headers
        for row in reader:
            _, created = ImPair.objects.get_or_create(
                island=row[0],
                collection_id=row[1],
                im1id0 = row[2],
                im1id1 = row[3],
                im2id0 = row[4],
                im2id1 = row[5],
                )
            if not created:
                duplicate_links.append(row)
        duplicate_links_np = np.asarray(duplicate_links)
        np.savetxt("edge/static/human_links_01232021_duplicate.csv", duplicate_links_np, delimiter=",", fmt='%s')

    return redirect('edge:select_island')

def create_duplicates(request):
    with open("edge/static/human_links_01232021_duplicate.csv") as f:
        reader = csv.reader(f)
        next(reader, None) # Skip the headers
        for row in reader:
            _, created = ImPair.objects.get_or_create(
                island=row[0],
                collection_id=row[1],
                im1id0 = row[2],
                im1id1 = row[3],
                im2id0 = row[4],
                im2id1 = row[5],
                linked = False
                )

    return redirect('edge:select_island')

def change_island_name(request):
    ImPair.objects.filter(island='Dominica').update(island="dominica")
    ImPair.objects.filter(island='Montserrat').update(island="montserrat")
    return redirect('edge:select_island')

### HELPER FUNCTIONS

def get_next_pair(island):
    unlinked_pairs = ImPair.objects.filter(linked=False, island=island)
    if unlinked_pairs.count() == 0:
        return [None, None, None]
    for i in range(unlinked_pairs.count()):
        pair = unlinked_pairs[i]
        im1_name = "NCAP/" + pair.island + "/" + pair.collection_id + "_" + str(f'{pair.im1id0:04}') + "/" + \
            pair.collection_id + "_" + str(f'{pair.im1id0:04}') + "_" + str(f'{pair.im1id1:04}') + ".jpg"
        im2_name = "NCAP/" + pair.island + "/" + pair.collection_id + "_" + str(f'{pair.im2id0:04}') + "/" + \
            pair.collection_id + "_" + str(f'{pair.im2id0:04}') + "_" + str(f'{pair.im2id1:04}') + ".jpg"
        if os.path.exists("edge/static/" + im1_name) and os.path.exists("edge/static/" + im2_name):
            return [pair.id, im1_name, im2_name]
    return [None, None, None]

