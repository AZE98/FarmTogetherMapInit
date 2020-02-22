# Farm Together 一起玩农场 MapInit 地图生成器

## 目录结构说明

data_json.py：原数据json格式规范化，原数据字符串和python的json互转。

main.py：脚本入口

map_init.py：图片转地图功能

undata.py：数据文件解压缩（与字符串的互转）

requirements.txt：依赖说明文件，可以通过pip install -r requirements.txt 快速安装依赖

## 使用说明

1. 准备好存档和图片的路径；
2. 下载本仓库下项目代码并安装第三方库；
3. 运行main.py；
4. 按照提示说明输入存档路径和图片路径执行即可。

## 其他说明

1. 欢迎大家下载使用，脚本的可读性、可扩展性、容错率都还有待改进，但是正常操作一般不会有问题，欢迎大家提issue。
2. 本程序提供了一些小工具，如数据文件的读取以及数据文件和json的互转，欢迎大家基于这些进行扩展。
3. 有其他问题可联系@ jwz1998@qq.com