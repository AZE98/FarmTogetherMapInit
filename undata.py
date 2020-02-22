# coding=utf-8
import gzip
import io


def farm_data_read(farm_data_path):
    return io.TextIOWrapper(gzip.open(farm_data_path, "rb"), encoding='utf-8-sig').read()


def farm_data_wirte(farm_data_path, farm_data_str):
    return io.TextIOWrapper(gzip.open(farm_data_path, "wb"), encoding='utf-8-sig').write(farm_data_str)


def backup_data(farm_data_path):
    try:
        temp_data = farm_data_read(farm_data_path)

        farm_data_wirte(farm_data_path+".bak", temp_data)
        return True
    except IOError:
        print("读取或写入失败，请重试。")
        return False


if __name__ == '__main__':
    str_data1 = "test string"
    str_data2 = farm_data_read("./farm_10 - 副本.data")
    # farm_data_wirte("./farm_10.data", str_data1)
    farm_data_wirte("./farm_10.data", str_data2)
