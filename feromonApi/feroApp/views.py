from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response

import os
from django.http import JsonResponse
import urllib.request as urllib
import numpy as np
#import main detectron function
from .detectron.bug_detectron import get_bug


def feromon_view(request):
    if request.method == 'GET':
        try:
            url=request.GET['imgurl']
            bug_result=get_bug(url)
            return JsonResponse(bug_result)
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