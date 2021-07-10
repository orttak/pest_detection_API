from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from django.http import HttpResponse

import os
from django.http import JsonResponse
import urllib.request as urllib
import numpy as np
#import main detectron function
from .detectron.bug_detectron import get_bug
from .detectron.corn_counter import corn_inference
from .detectron.jsonToGeojson import jsonToGeojson
from .detectron.geojsonToJson import get_json_from_geojson

def feromon_view(request):
    if request.method == 'GET':
        try:
            url=request.GET['imgurl']
            bug_result=get_bug(url)
            return JsonResponse(bug_result)
        except:
            return JsonResponse({'Response':'Bad request'})

def corn_view(request):
    if request.method == 'GET':
        try:
            img_h_url=request.GET['img_h_url']
            img_w_url=request.GET['img_w_url']
            json_h,json_w,k_h=corn_inference(img_h_url=img_h_url,img_w_url=img_w_url)
            return JsonResponse({'corn_height':json_h,'corn_width':json_w,'numberOfKernel':k_h})
        except:
            return JsonResponse({'Response':'Bad request'})

def jsontogeojson(request):
    if request.method == 'GET':
        try:
            json_obj=request.GET['imgjson']
            py_json_obj=f'{json_obj}'
            geojson_result=jsonToGeojson(py_json_obj)            
            return HttpResponse(geojson_result, content_type="application/json")
        except:
            return JsonResponse({'Response':'Bad request'})

def geojsontojson(request):
    if request.method == 'GET':
        try:
            url=request.GET['imgurl']
            json_obj=request.GET['geojson']
            
            py_json_obj=f'{json_obj}'
            geojson_result=get_json_from_geojson(url=url,vec_geojson=py_json_obj)

            return JsonResponse(geojson_result)
            #return JsonResponse({'Response':'heyyyyyyyyy'})
        except:
            return JsonResponse({'Response':'Bad request'})

'''
#sample url
https://doktarstorage.blob.core.windows.net/feromon/PheromoneTrap_14022071_20201014075945.jpg
https://doktarstorage.blob.core.windows.net/feromon/PheromoneTrap_14022071_20201013075959.jpg
https://doktarstorage.blob.core.windows.net/feromon/PheromoneTrap_14022071_20201012200032.jpg
https://doktarstorage.blob.core.windows.net/feromon/PheromoneTrap_14022071_20201011200025.jpg
https://doktarstorage.blob.core.windows.net/feromon/PheromoneTrap_14022071_20201010200037.jpg
https://doktarstorage.blob.core.windows.net/feromon/PheromoneTrap_14022071_20201009200018.jpg
'''