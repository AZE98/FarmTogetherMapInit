# coding=utf-8
from PIL import Image
from PIL import ImageFilter
import numpy as np

from data_json import *


def get_edge(image):
    return image.filter(ImageFilter.CONTOUR)


def check_image(image):
    if image.size[0] / image.size[1] == 2:
        return True
    else:
        return False


def img2arr(image, is_one=False):
    if not check_image(image):
        print("Error: Img size error")
        return
    if is_one:
        image = image.resize((40, 20))
    else:
        image = image.resize((280, 140))
    image = image.convert('L')  # 灰度图像

    # arr = np.asarray(image)
    # for y in range(image.size[1]):
    #     for x in range(image.size[0]):
    #         if arr[y][x] < 230:
    #             print("*", end="")
    #         else:
    #             print(" ", end="")
    #     print()

    return np.asarray(image)


def gen_block(x, y, image_array, chunks_json, replace, threshold=230, is_one=False):
    chunks_json['ChunkId'] = 'Flat_Chunk'
    json_temp = chunks_json['Tiles']
    if is_one:  # 是整张图
        x, y = 0, 7-1
    for m in range(40):
        for n in range(20):
            img_x = 40 * x + m
            img_y = 20 * (7-1-y) + (19-n)
            if image_array[img_y][img_x] < threshold:
                if len(json_temp[20*m + n]) < 2:
                    json_temp[20*m + n]['state'] = replace['state']
                    json_temp[20*m + n]['contents'] = replace['contents']

    return chunks_json


def gen_all_map(image_array, chunks_json, replace, threshold=230):
    for x in range(7):
        for y in range(7):
            chunks_json[7 * x + y] = gen_block(x, y, image_array, chunks_json[7 * x + y], replace, threshold=threshold)
    return chunks_json


def unlock_all(farm_root):
    for x in range(7):
        for y in range(7):
            farm_root["Chunks"][7 * x + y]["Unlocked"] = 'true'
            farm_root["Chunks"][7 * x + y]["ChunkId"] = 'Flat_Chunk'

    for building_item in farm_root["Buildings"]:
        if building_item["id"] == "InternalBuildingUnlockChunk" or "DecorationHayBales":
            building_id = building_item["building_id"]
            for x in range(49):
                for y in range(800):
                    print(x, y)
                    if len(farm_root["Chunks"][x]["Tiles"][y]) == 1:
                        continue
                    try:
                        if farm_root["Chunks"][x]["Tiles"][y]["contents"]["building_id"] == building_id:
                            del farm_root["Chunks"][x]["Tiles"][y]["contents"]
                            del farm_root["Chunks"][x]["Tiles"][y]["state"]
                    except KeyError:
                        continue
            farm_root["Buildings"].remove(building_item)

    return farm_root


def clear_all(farm_root):
    farm_root["Buildings"] = []
    farm_root["Animals"] = []
    farm_root["Ponds"] = []
    for wrap in range(49):
        for x in range(40):
            for y in range(20):
                farm_root["Chunks"][wrap]["Tiles"][x*20+y] = {"tile": str(x)+","+str(y)}

    return farm_root


def clear_all_except_spawnpoint(farm_root):

    for building_item in farm_root["Buildings"]:
        if building_item["id"] != "InternalBuildingSpawnPoint":
            farm_root["Buildings"].remove(building_item)
    spawnpoint_id = farm_root["Buildings"][0]["building_id"]
    farm_root["Animals"] = []
    farm_root["Ponds"] = []
    for wrap in range(49):
        for x in range(40):
            for y in range(20):
                if len(farm_root["Chunks"][wrap]["Tiles"][x*20+y]) > 1:
                    try:
                        if farm_root["Chunks"][wrap]["Tiles"][x*20+y]["contents"]["building_id"] != spawnpoint_id:
                            farm_root["Chunks"][wrap]["Tiles"][x*20+y]["tile"] = str(x)+","+str(y)
                    except KeyError:
                        farm_root["Chunks"][wrap]["Tiles"][x*20+y] = {"tile": str(x)+","+str(y)}
    return farm_root


if __name__ == '__main__':
    root = data_file2json("./farm_9.data")
    root = unlock_all(root)
    root = clear_all(root)
    replace_item = {"state": 3, "contents": {"type": 7, "id": "RoadGrass"}}
    root["Chunks"][3*7+3] = gen_block(3, 3, img2arr(Image.open("./test.png"), is_one=True),
                                      root["Chunks"][3*7+3], replace_item, threshold=230, is_one=True)
    json2data_file("./farm_9.data", root)
