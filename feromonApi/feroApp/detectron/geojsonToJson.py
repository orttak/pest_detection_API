import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import json
import cv2 
import geopandas as gpd
import numpy as np 
import rasterio
import fiona
import matplotlib as mpl
import geopandas as gpd
from shapely.geometry import Polygon

import urllib.request

def getBBOXfromShapely(feature):
    ##### get bounding box (in coco format) from shapely polygon object (x1,y1,h,w)
    return [feature.bounds[0],feature.bounds[1],feature.bounds[2]-feature.bounds[0],feature.bounds[3]- feature.bounds[1]]

def get_exterior_poly(input_poly):
    ### get the exterior of polygon (ignore this function)
    if str(type(input_poly)) == "<class 'shapely.geometry.multipolygon.MultiPolygon'>":
        input_poly = input_poly[0]
    lst = list(input_poly.exterior.coords)
    list_ = [e for l in lst for e in l]
    return list_

def getBBOXfromShapely2(feature):
    ## ger the bounding box in other format (for showing in HTML)(x1,y1,x2,y2,x3,y3,x4,y4)
    return [feature.bounds[0],feature.bounds[1],feature.bounds[2],feature.bounds[1],feature.bounds[2], feature.bounds[3],feature.bounds[0], feature.bounds[3]]
def get_inv_transform():
    ## get the affine transform (fixed for now)
    return [1.0, 0.0, -0.0, -1.0, -0.5, -0.5]

def get_json_from_geojson(url,vec_geojson):
    ##inputs: 
    ##url:url to image, vec_geojson:  geojson
    
    ## read image
    input_jpeg=urllib.request.urlretrieve(url,'inputfromgeojson.jpeg')
    im=cv2.imread(input_jpeg[0])
    
    #imagename
    image_name=url.split('/')[-1]
    
    ## define projection (EPSG:4326)
    #CRC = rasterio.crs.CRS.from_string('EPSG:4326')
    
    ##get inverse transform  
    inv_transfrom = get_inv_transform()
    
    ## read the geojson as geoseries 
    poly_gseries = gpd.GeoDataFrame.from_file(vec_geojson).dropna( inplace=False).reset_index()
    
    ### project the geoseries to matrix coordinates 
    test_matcoor_w = poly_gseries.affine_transform(inv_transfrom)

    ## read reference class names and ids file and convetr them to coco format
    pth_json = os.path.join(os.path.dirname(os.path.realpath(__file__)),"Doktar_Feromon_Referans_v05.json")

    with open(pth_json,encoding="utf-8") as json_file:
        ref_json = json.load(json_file) 
    mycat ={}
    for ref in ref_json: 
        mycat[ref["TagName"]] = int(ref["ClassId"])    
    
    mycat2 = []
    ### dictionary for all images in COCO format 
    bugs_coco = {"info": {},"licenses": [],"categories": [mycat2],"images": [], "annotations": []  }
    #print(bugs_coco)
    for i,k in enumerate(mycat.keys()):
        if(mycat[k]>0):
            mycat2.append({ "id":int(mycat[k])  ,"name": str(k),"supercategory": "bugs" })
        else: 
            mycat2.append({ "id": int(mycat[k]) ,"name":  str(k),"supercategory": "other" })   
   #################
    ### get size of the image
    X,Y,C = im.shape  

    ##start counter for images 
    k = 1
    
    ### temporary dictionary to hold the info of each image  
    temp = {}
    temp = {"id" : k ,"width": Y, "height":X, "file_name":image_name}#poly_gseries["ImageID"][0]


    ### append image info to main dictionary
    bugs_coco["images"].append(temp)
    
    ### start counter for objects 
    h = 0
    
    ### for each object in the geoseries 
    for i,g in enumerate(poly_gseries["TagName"]):
        ### temp2 to hold info og object g 
        #temp2 = {"id": h, "image_id": int(k) , "category_id": mycat[poly_gseries["TagName"][i]] ,"bbox":getBBOXfromShapely(test_matcoor_w[i]),"iscrowd": 0,"segmentation":get_exterior_poly(test_matcoor_w[i]),"M_BBOX": getBBOXfromShapely2(test_matcoor_w[i])}
        #remove segmentation part
        temp2 = {"id": h, "iscrowd": 0, "image_id": int(k) , "category_id": mycat[poly_gseries["TagName"][i]] ,"bbox":getBBOXfromShapely(test_matcoor_w[i]),"M_BBOX": getBBOXfromShapely2(test_matcoor_w[i])}

        
        ##increment object counter 
        h = h + 1
        
        ### add object to final dictionary
        bugs_coco["annotations"].append(temp2)
    
    #print(bugs_coco["categories"])
    bugs_coco["categories"] = bugs_coco["categories"][0]
    #print(bugs_coco)
    return bugs_coco




#url1='https://doktar.azureedge.net/feromon/PheromoneTrap_14021014_20210123200213.jpg'
#dd='{"type": "FeatureCollection", "features": [{"id": "0", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[305.61407470703125, -783.2178955078125], [353.96453857421875, -783.2178955078125], [353.96453857421875, -846.548828125], [305.61407470703125, -846.548828125], [305.61407470703125, -783.2178955078125]]]}}, {"id": "1", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[169.9463348388672, -451.62384033203125], [232.59153747558594, -451.62384033203125], [232.59153747558594, -515.6913452148438], [169.9463348388672, -515.6913452148438], [169.9463348388672, -451.62384033203125]]]}}, {"id": "2", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[248.68508911132812, -726.50537109375], [303.994140625, -726.50537109375], [303.994140625, -819.22509765625], [248.68508911132812, -819.22509765625], [248.68508911132812, -726.50537109375]]]}}, {"id": "3", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[205.11138916015625, -862.5596313476562], [244.3463134765625, -862.5596313476562], [244.3463134765625, -904.0374145507812], [205.11138916015625, -904.0374145507812], [205.11138916015625, -862.5596313476562]]]}}, {"id": "4", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[832.296142578125, -173.5282440185547], [863.4767456054688, -173.5282440185547], [863.4767456054688, -204.7923583984375], [832.296142578125, -204.7923583984375], [832.296142578125, -173.5282440185547]]]}}, {"id": "5", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[107.95372009277344, -282.17437744140625], [142.4915771484375, -282.17437744140625], [142.4915771484375, -323.360595703125], [107.95372009277344, -323.360595703125], [107.95372009277344, -282.17437744140625]]]}}, {"id": "6", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[436.5891418457031, -640.7882690429688], [492.60748291015625, -640.7882690429688], [492.60748291015625, -690.920166015625], [436.5891418457031, -690.920166015625], [436.5891418457031, -640.7882690429688]]]}}, {"id": "7", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[678.70458984375, -519.43017578125], [733.0768432617188, -519.43017578125], [733.0768432617188, -583.5034790039062], [678.70458984375, -583.5034790039062], [678.70458984375, -519.43017578125]]]}}, {"id": "8", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[157.6786346435547, -1076.1314697265625], [196.6774139404297, -1076.1314697265625], [196.6774139404297, -1109.2860107421875], [157.6786346435547, -1109.2860107421875], [157.6786346435547, -1076.1314697265625]]]}}, {"id": "9", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[277.724609375, -1087.8682861328125], [333.92230224609375, -1087.8682861328125], [333.92230224609375, -1147.8043212890625], [277.724609375, -1147.8043212890625], [277.724609375, -1087.8682861328125]]]}}, {"id": "10", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[155.1446990966797, -849.503662109375], [205.90216064453125, -849.503662109375], [205.90216064453125, -902.8353271484375], [155.1446990966797, -902.8353271484375], [155.1446990966797, -849.503662109375]]]}}, {"id": "11", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[728.1505126953125, -983.5115966796875], [785.7594604492188, -983.5115966796875], [785.7594604492188, -1034.9847412109375], [728.1505126953125, -1034.9847412109375], [728.1505126953125, -983.5115966796875]]]}}, {"id": "12", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[145.983642578125, -852.8843383789062], [246.49160766601562, -852.8843383789062], [246.49160766601562, -907.0652465820312], [145.983642578125, -907.0652465820312], [145.983642578125, -852.8843383789062]]]}}, {"id": "13", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[1334.3265380859375, -983.5945434570312], [1361.6119384765625, -983.5945434570312], [1361.6119384765625, -1024.0187377929688], [1334.3265380859375, -1024.0187377929688], [1334.3265380859375, -983.5945434570312]]]}}, {"id": "14", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[1456.531005859375, -1033.895751953125], [1490.7952880859375, -1033.895751953125], [1490.7952880859375, -1077.375732421875], [1456.531005859375, -1077.375732421875], [1456.531005859375, -1033.895751953125]]]}}, {"id": "15", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[396.61688232421875, -1144.54345703125], [460.09674072265625, -1144.54345703125], [460.09674072265625, -1192.2313232421875], [396.61688232421875, -1192.2313232421875], [396.61688232421875, -1144.54345703125]]]}}, {"id": "16", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[744.3896484375, -584.823486328125], [799.8880615234375, -584.823486328125], [799.8880615234375, -622.332275390625], [744.3896484375, -622.332275390625], [744.3896484375, -584.823486328125]]]}}, {"id": "17", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[723.73583984375, -984.674560546875], [783.027587890625, -984.674560546875], [783.027587890625, -1028.37744140625], [723.73583984375, -1028.37744140625], [723.73583984375, -984.674560546875]]]}}, {"id": "18", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[396.80816650390625, -1147.762939453125], [454.8951721191406, -1147.762939453125], [454.8951721191406, -1188.5711669921875], [396.80816650390625, -1188.5711669921875], [396.80816650390625, -1147.762939453125]]]}}, {"id": "19", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[536.9238891601562, -362.9486389160156], [690.8152465820312, -362.9486389160156], [690.8152465820312, -492.86346435546875], [536.9238891601562, -492.86346435546875], [536.9238891601562, -362.9486389160156]]]}}, {"id": "20", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[1448.092041015625, -0.871729850769043], [1534.6046142578125, -0.871729850769043], [1534.6046142578125, -57.83993434906006], [1448.092041015625, -57.83993434906006], [1448.092041015625, -0.871729850769043]]]}}, {"id": "21", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[1327.379150390625, -279.2003479003906], [1409.9200439453125, -279.2003479003906], [1409.9200439453125, -405.5118103027344], [1327.379150390625, -405.5118103027344], [1327.379150390625, -279.2003479003906]]]}}, {"id": "22", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[560.99169921875, -387.65643310546875], [654.0018920898438, -387.65643310546875], [654.0018920898438, -462.03118896484375], [560.99169921875, -462.03118896484375], [560.99169921875, -387.65643310546875]]]}}, {"id": "23", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[438.0329895019531, -644.2252807617188], [486.733154296875, -644.2252807617188], [486.733154296875, -688.7120361328125], [438.0329895019531, -688.7120361328125], [438.0329895019531, -644.2252807617188]]]}}, {"id": "24", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[742.6484375, -584.563720703125], [797.8460693359375, -584.563720703125], [797.8460693359375, -621.6083374023438], [742.6484375, -621.6083374023438], [742.6484375, -584.563720703125]]]}}, {"id": "25", "type": "Feature", "properties": {"TagName": "Cisim"}, "geometry": {"type": "Polygon", "coordinates": [[[773.7288208007812, -573.0732421875], [965.8976440429688, -573.0732421875], [965.8976440429688, -732.9346313476562], [773.7288208007812, -732.9346313476562], [773.7288208007812, -573.0732421875]]]}}]}'
#print(get_json_from_geojson(url=url1,vec_geojson=dd))
#get_json_from_geojson(url=url1,vec_geojson=dd)