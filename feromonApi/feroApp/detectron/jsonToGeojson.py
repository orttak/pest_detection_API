from shapely.geometry import Polygon,MultiPolygon
import numpy as np
from shapely.affinity import affine_transform 
import geopandas
import sys
import os
import numpy as np
import json
import pandas as pd


def jsonToGeojson(input_json,):
    #read input json
    json_file=json.loads(f'{input_json}')
    inv_map = {}
    for c in json_file['categories']: 
        inv_map[c['id']] = c['name']

    ### affine inverse transform 
    A_est_inv = [1.0, 0.0, -0.0, -1.0, -0.5, -0.5]

    ### empty list 
    polygons_list = []

    ### empty class name list 
    class_name_list= []

    ### temp matrix to hold info
    temp_matrix = np.zeros((4,2))
    temp_matrix.shape

    ## for each annotation in json file 
    for ann in json_file['annotations']:
        ### put invalid annotations in catagory 901 
        if np.sum(np.asarray(list(inv_map.keys()))==ann['category_id'])== 0:
            ann['category_id'] = 901

        ### get bounding box of ann 
        x,y,h,w = ann['bbox']

        ### find all corner point of bbox 
        x1 = x 
        x2 = x +  h
        y1 = y 
        y2 = y + w

        ann['M_BBOX'] =  [x1,y1,x2,y1,x2,y2,x1,y2]

        ## define them as array 
        bbox_array = np.asarray( ann['M_BBOX'] )
        bbox_array = np.squeeze(bbox_array)
        bbox_array.shape
        bbox_array[0::2,]
        bbox_array[1::2,]
        temp_matrix[:,0]= bbox_array[0::2,]
        temp_matrix[:,1]= bbox_array[1::2,]
        bbox_array = temp_matrix.copy()
        ### define them as polygon 
        polygon_bbox = Polygon(bbox_array)
        ## affine transrom to see them in QGIS 
        affine_object = affine_transform(polygon_bbox,A_est_inv )
        #print(AT)
        ## add polygon to the list 
        polygons_list.append(affine_object )
        ### add the class name 
        class_name_list.append(inv_map[ann['category_id']])

    ## creat dataframe 
    df = pd.DataFrame({'geometry':polygons_list,'TagName':class_name_list})
    ### creat geopandas dataframe 
    geo_dataframe = geopandas.GeoDataFrame(df)
    ### define projection  and project dataframe 
    geo_dataframe.crs = 'EPSG:4326'
    geo_dataframe= geo_dataframe.to_crs('EPSG:4326')

    #geojson_result=json.dumps(geo_dataframe.to_json())
    geojson_result=geo_dataframe.to_json()

    return geojson_result


test='{"info": {"description": "my-project-name"}, "licenses": [], "images": [{"id": 1, "width": 1600, "height": 1200, "file_name": "PheromoneTrap_14021014_20210123200213.jpg"}], "annotations": [{"id": 0, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [306.11407470703125, 782.7178955078125, 48.3504638671875, 63.3309326171875], "M_BBOX": [306.11407470703125, 782.7178955078125, 354.46453857421875, 782.7178955078125, 354.46453857421875, 846.048828125, 306.11407470703125, 846.048828125]}, {"id": 1, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [170.4463348388672, 451.12384033203125, 62.64520263671875, 64.0675048828125], "M_BBOX": [170.4463348388672, 451.12384033203125, 233.09153747558594, 451.12384033203125, 233.09153747558594, 515.1913452148438, 170.4463348388672, 515.1913452148438]}, {"id": 2, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [249.18508911132812, 726.00537109375, 55.309051513671875, 92.7197265625], "M_BBOX": [249.18508911132812, 726.00537109375, 304.494140625, 726.00537109375, 304.494140625, 818.72509765625, 249.18508911132812, 818.72509765625]}, {"id": 3, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [205.61138916015625, 862.0596313476562, 39.23492431640625, 41.477783203125], "M_BBOX": [205.61138916015625, 862.0596313476562, 244.8463134765625, 862.0596313476562, 244.8463134765625, 903.5374145507812, 205.61138916015625, 903.5374145507812]}, {"id": 4, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [832.796142578125, 173.0282440185547, 31.18060302734375, 31.264114379882812], "M_BBOX": [832.796142578125, 173.0282440185547, 863.9767456054688, 173.0282440185547, 863.9767456054688, 204.2923583984375, 832.796142578125, 204.2923583984375]}, {"id": 5, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [108.45372009277344, 281.67437744140625, 34.53785705566406, 41.18621826171875], "M_BBOX": [108.45372009277344, 281.67437744140625, 142.9915771484375, 281.67437744140625, 142.9915771484375, 322.860595703125, 108.45372009277344, 322.860595703125]}, {"id": 6, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [437.0891418457031, 640.2882690429688, 56.018341064453125, 50.13189697265625], "M_BBOX": [437.0891418457031, 640.2882690429688, 493.10748291015625, 640.2882690429688, 493.10748291015625, 690.420166015625, 437.0891418457031, 690.420166015625]}, {"id": 7, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [679.20458984375, 518.93017578125, 54.37225341796875, 64.07330322265625], "M_BBOX": [679.20458984375, 518.93017578125, 733.5768432617188, 518.93017578125, 733.5768432617188, 583.0034790039062, 679.20458984375, 583.0034790039062]}, {"id": 8, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [158.1786346435547, 1075.6314697265625, 38.998779296875, 33.154541015625], "M_BBOX": [158.1786346435547, 1075.6314697265625, 197.1774139404297, 1075.6314697265625, 197.1774139404297, 1108.7860107421875, 158.1786346435547, 1108.7860107421875]}, {"id": 9, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [278.224609375, 1087.3682861328125, 56.19769287109375, 59.93603515625], "M_BBOX": [278.224609375, 1087.3682861328125, 334.42230224609375, 1087.3682861328125, 334.42230224609375, 1147.3043212890625, 278.224609375, 1147.3043212890625]}, {"id": 10, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [155.6446990966797, 849.003662109375, 50.75746154785156, 53.3316650390625], "M_BBOX": [155.6446990966797, 849.003662109375, 206.40216064453125, 849.003662109375, 206.40216064453125, 902.3353271484375, 155.6446990966797, 902.3353271484375]}, {"id": 11, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [728.6505126953125, 983.0115966796875, 57.60894775390625, 51.47314453125], "M_BBOX": [728.6505126953125, 983.0115966796875, 786.2594604492188, 983.0115966796875, 786.2594604492188, 1034.4847412109375, 728.6505126953125, 1034.4847412109375]}, {"id": 12, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [146.483642578125, 852.3843383789062, 100.50796508789062, 54.180908203125], "M_BBOX": [146.483642578125, 852.3843383789062, 246.99160766601562, 852.3843383789062, 246.99160766601562, 906.5652465820312, 146.483642578125, 906.5652465820312]}, {"id": 13, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [1334.8265380859375, 983.0945434570312, 27.285400390625, 40.4241943359375], "M_BBOX": [1334.8265380859375, 983.0945434570312, 1362.1119384765625, 983.0945434570312, 1362.1119384765625, 1023.5187377929688, 1334.8265380859375, 1023.5187377929688]}, {"id": 14, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [1457.031005859375, 1033.395751953125, 34.2642822265625, 43.47998046875], "M_BBOX": [1457.031005859375, 1033.395751953125, 1491.2952880859375, 1033.395751953125, 1491.2952880859375, 1076.875732421875, 1457.031005859375, 1076.875732421875]}, {"id": 15, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [397.11688232421875, 1144.04345703125, 63.4798583984375, 47.6878662109375], "M_BBOX": [397.11688232421875, 1144.04345703125, 460.59674072265625, 1144.04345703125, 460.59674072265625, 1191.7313232421875, 397.11688232421875, 1191.7313232421875]}, {"id": 16, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [744.8896484375, 584.323486328125, 55.4984130859375, 37.5087890625], "M_BBOX": [744.8896484375, 584.323486328125, 800.3880615234375, 584.323486328125, 800.3880615234375, 621.832275390625, 744.8896484375, 621.832275390625]}, {"id": 17, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [724.23583984375, 984.174560546875, 59.291748046875, 43.702880859375], "M_BBOX": [724.23583984375, 984.174560546875, 783.527587890625, 984.174560546875, 783.527587890625, 1027.87744140625, 724.23583984375, 1027.87744140625]}, {"id": 18, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [397.30816650390625, 1147.262939453125, 58.087005615234375, 40.8082275390625], "M_BBOX": [397.30816650390625, 1147.262939453125, 455.3951721191406, 1147.262939453125, 455.3951721191406, 1188.0711669921875, 397.30816650390625, 1188.0711669921875]}, {"id": 19, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [537.4238891601562, 362.4486389160156, 153.891357421875, 129.91482543945312], "M_BBOX": [537.4238891601562, 362.4486389160156, 691.3152465820312, 362.4486389160156, 691.3152465820312, 492.36346435546875, 537.4238891601562, 492.36346435546875]}, {"id": 20, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [1448.592041015625, 0.37172985076904297, 86.5125732421875, 56.968204498291016], "M_BBOX": [1448.592041015625, 0.37172985076904297, 1535.1046142578125, 0.37172985076904297, 1535.1046142578125, 57.33993434906006, 1448.592041015625, 57.33993434906006]}, {"id": 21, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [1327.879150390625, 278.7003479003906, 82.5408935546875, 126.31146240234375], "M_BBOX": [1327.879150390625, 278.7003479003906, 1410.4200439453125, 278.7003479003906, 1410.4200439453125, 405.0118103027344, 1327.879150390625, 405.0118103027344]}, {"id": 22, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [561.49169921875, 387.15643310546875, 93.01019287109375, 74.374755859375], "M_BBOX": [561.49169921875, 387.15643310546875, 654.5018920898438, 387.15643310546875, 654.5018920898438, 461.53118896484375, 561.49169921875, 461.53118896484375]}, {"id": 23, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [438.5329895019531, 643.7252807617188, 48.700164794921875, 44.48675537109375], "M_BBOX": [438.5329895019531, 643.7252807617188, 487.233154296875, 643.7252807617188, 487.233154296875, 688.2120361328125, 438.5329895019531, 688.2120361328125]}, {"id": 24, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [743.1484375, 584.063720703125, 55.1976318359375, 37.04461669921875], "M_BBOX": [743.1484375, 584.063720703125, 798.3460693359375, 584.063720703125, 798.3460693359375, 621.1083374023438, 743.1484375, 621.1083374023438]}, {"id": 25, "iscrowd": 0, "image_id": 1, "category_id": 902, "bbox": [774.2288208007812, 572.5732421875, 192.1688232421875, 159.86138916015625], "M_BBOX": [774.2288208007812, 572.5732421875, 966.3976440429688, 572.5732421875, 966.3976440429688, 732.4346313476562, 774.2288208007812, 732.4346313476562]}], "categories": [{"id": 32, "name": "AkdenizCamKabukBocegi", "supercategory": "bugs"}, {"id": 13, "name": "AkdenizMeyveSinegi", "supercategory": "bugs"}, {"id": 39, "name": "AkdenizOrmanBahcivani", "supercategory": "bugs"}, {"id": 40, "name": "AltiDisliCamKabukBocegi", "supercategory": "bugs"}, {"id": 47, "name": "AltinGozluBocek", "supercategory": "bugs"}, {"id": 44, "name": "Ari", "supercategory": "bugs"}, {"id": 27, "name": "ArpaGuvesi", "supercategory": "bugs"}, {"id": 22, "name": "BaklaZinni", "supercategory": "bugs"}, {"id": 28, "name": "BugdayBiti", "supercategory": "bugs"}, {"id": 38, "name": "BuyukOrmanBahcivani", "supercategory": "bugs"}, {"id": 35, "name": "CamKeseBocegi", "supercategory": "bugs"}, {"id": 36, "name": "CamKulturHortumluBocegi", "supercategory": "bugs"}, {"id": 34, "name": "CamSurgunBukucusu", "supercategory": "bugs"}, {"id": 5, "name": "CicekTripsi", "supercategory": "bugs"}, {"id": 25, "name": "DegirmenGuvesi", "supercategory": "bugs"}, {"id": 11, "name": "DoguMeyveGuvesi", "supercategory": "bugs"}, {"id": 4, "name": "DomatesGuvesi", "supercategory": "bugs"}, {"id": 29, "name": "ElbiseGuvesi", "supercategory": "bugs"}, {"id": 21, "name": "ElmaGovdeKurdu", "supercategory": "bugs"}, {"id": 2, "name": "ElmaIcKurdu", "supercategory": "bugs"}, {"id": 12, "name": "ElmaYaprakBukeni", "supercategory": "bugs"}, {"id": 19, "name": "ErikIcKurdu", "supercategory": "bugs"}, {"id": 900, "name": "Feromon", "supercategory": "other"}, {"id": 42, "name": "FindikDalkiran", "supercategory": "bugs"}, {"id": 30, "name": "GoknarBuyukKabukBocegi", "supercategory": "bugs"}, {"id": 10, "name": "HarnupGuvesi", "supercategory": "bugs"}, {"id": 17, "name": "KirazSinegi", "supercategory": "bugs"}, {"id": 23, "name": "KirmiziPalmiyeBocegi", "supercategory": "bugs"}, {"id": 15, "name": "KizilAgacKurdu", "supercategory": "bugs"}, {"id": 41, "name": "KucukGoknarKabukBocegi", "supercategory": "bugs"}, {"id": 37, "name": "KucukOrmanBahcivani", "supercategory": "bugs"}, {"id": 24, "name": "KuruMeyveGuvesi", "supercategory": "bugs"}, {"id": 16, "name": "LimonCicekGuvesi", "supercategory": "bugs"}, {"id": 45, "name": "MisirKocanKurdu", "supercategory": "bugs"}, {"id": 33, "name": "OnikiDisliCamKabukBocegi", "supercategory": "bugs"}, {"id": 7, "name": "PamukPembeKurt", "supercategory": "bugs"}, {"id": 8, "name": "PamukYaprakKurdu", "supercategory": "bugs"}, {"id": 6, "name": "PatatesGuvesi", "supercategory": "bugs"}, {"id": 1, "name": "SalkimGuvesi", "supercategory": "bugs"}, {"id": 20, "name": "SariAgacKurdu", "supercategory": "bugs"}, {"id": 18, "name": "SeftaliGuvesi", "supercategory": "bugs"}, {"id": 43, "name": "SekizDisliCamKabukBocegi", "supercategory": "bugs"}, {"id": 46, "name": "Sinek", "supercategory": "bugs"}, {"id": 48, "name": "AltinGozluYesilBocek", "supercategory": "bugs"}, {"id": 901, "name": "Tanimsiz", "supercategory": "other"}, {"id": 26, "name": "TatliKurt", "supercategory": "bugs"}, {"id": 31, "name": "YatayDisliGoknarKabukBocegi", "supercategory": "bugs"}, {"id": 9, "name": "YesilKurt", "supercategory": "bugs"}, {"id": 3, "name": "ZeytinGuvesi", "supercategory": "bugs"}, {"id": 14, "name": "ZeytinSinegi", "supercategory": "bugs"}, {"id": 902, "name": "Cisim", "supercategory": "other"}]}'
print(jsonToGeojson(test))

