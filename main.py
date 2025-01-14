# coding=utf-8
from map_init import *


def main(farm_data_path):
    try:
        data_root = data_file2json(farm_data_path)
    except FileNotFoundError:
        print("找不到改存档，请重试。")
        return
    new_replace_item = {"state": 3, "contents": {"type": 7, "id": "RoadGrass"}}

    while True:
        choice = input('''-----------------------
！请注意：本脚本只适用于平原地图。
请输入数字选择功能：
1. 备份存档(会覆盖之前存在的备份存档)
2. 解锁全图
3. 清空全图(清空全图前请先解锁全图)
4. 绘制地图(绘制前请清空全图)
5. 保存存档
0. 重选存档
-----------------------\n''')
        if choice == "0":
            return

        elif choice == "1":
            backup_data(farm_data_path)
            print("存档备份成功！")

        elif choice == "2":
            data_root = unlock_all(data_root)
            print("已解锁全部地皮！")

        elif choice == "3":
            sub_choice = input("是否要保留主车站？（Y/N）\n0. 返回上一级\nY. 保留\nN. 不保留\n")
            if sub_choice == "y" or sub_choice == "Y":
                data_root = clear_all_except_spawnpoint(data_root)
            elif sub_choice == "n" or sub_choice == "N":
                data_root = clear_all(data_root)
            print("已清空全部地皮！")

        elif choice == "4":
            while True:
                img_path = input("请输入图片路径:（形式如C:/**/.../*.png）(输入0返回上一级)\n")
                if img_path == "0":
                    break
                try:
                    img = Image.open(img_path)
                except IOError:
                    print("图片加载错误，请重试！")
                    continue
                if check_image(img) is not None:

                    mode = input("请选择图片模式。\n"
                                 "1. 边缘模式(该模式可提取图片边缘进行绘制)\n"
                                 "2. 填充模式(该模式可将图片转为黑白图直接进行绘制)\n")
                    if mode == "1":
                        img = get_edge(img)
                    elif mode == "2":
                        pass
                    else:
                        print("指令无效，已默认设置为填充模式！")

                    real_threshold = input("请输入0到255的阈值，从黑到白为0-255，程序会将低于阈值的位置放置物品，"
                                           "填充地图。留空即为默认值230。\n")
                    if real_threshold == "":
                        real_threshold = 230

                    chunk_id = input("请输入ChunkId的值：\n")

                    data_root["Chunks"] = gen_all_map(img2arr(img), data_root["Chunks"],
                                                      new_replace_item, threshold=int(real_threshold), chunk_id=chunk_id)

                    print("地图已生成，请注意保存存档。")
                    break
                else:
                    print("图片加载错误，请重试！")

        elif choice == "5":
            json2data_file(farm_data_path, data_root)
            print("存档保存成功！")

        else:
            print("指令无效，请重试！")


if __name__ == '__main__':
    while True:
        data_path = input("请输入存档路径:（形式如C:/**/.../farm_*.data）（输入0即可退出程序）：\n")
        if data_path == "0":
            break
        main(data_path)
