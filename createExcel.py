import os
import math
import numpy as np
import cv2
from xlwt import *

def createExcel(data_path):
    # point_pixel = []
    data_list = []
    raw_data_path = '/media/queahren/DATA/服务外包大赛数据更新/训练数据'

    # target = []
    #   y0 : y轴基准值, y0_pixel : y轴像素基准值, p : 单位像素是多少y值。
    def fun2(txt_path, y0, y0_pixel, p, img):
        with open(txt_path, "r") as f:
            # with open("/Users/jsy/Desktop/data_set/point_pixel/curve_7_mask.txt","r") as f:
            file = f.readlines()
            for line in file:
                line = line.strip("\n")  # 去除末尾的换行符
                dd = line.split(',')  # 拆分为两个元素，再对每个元素实行类型转换
                temp = list(map(int, dd))
                data_list.append(temp)
            point_pixel = np.array(data_list)
        print(point_pixel)
        y_predict = []
        for point in point_pixel:
            # print(point[1])
            y_pixel = point[1]
            y = float((y_pixel - y0_pixel) * p + y0)
            y_predict.append(y)
            cv2.putText(img, '{:.2f}'.format(y), (point[0] + 2, point[1]), cv2.FONT_HERSHEY_DUPLEX, 0.25, (255, 0, 0))

        print(y_predict)
        # print("--------------result-----------------")

        return y_predict, img

    def cal_d(predict, real, k):
        # new_predict = predict.astype(type('float', (float,), {}))
        sum = 0
        for i in range(0, 5):
            tmp1 = float(real[i]) - float(predict[i])
            tmp2 = float(tmp1 / k)
            tmp3 = pow(tmp2, 2)
            sum = sum + tmp3
        result = math.sqrt(sum)
        return result

    def fun3(name, y_predict):
        # print("------------step3----------")
        x = name
        c = x.split('_')[0]
        # print(c)
        if (c == "curve"):
            path1 = os.path.join(raw_data_path, "img_train_曲线")
        else:
            path1 = os.path.join(raw_data_path, "img_train_折线")
        number = x.split('_')[1]
        path2 = os.path.join(path1, number)
        file = os.path.join(path2, "db.txt")
        with open(file, "r") as f:
            lines = f.readlines()
            k = int(lines[0])
            y_real_str = lines[1]
            y_real = [float(x) for x in y_real_str.split(',')]
            # for y in y_real:
            #     print(y)
        f.close()
        name = x.split('.')[0].split('_')[0] + '_' + x.split('.')[0].split('_')[1] + '_result'
        # print(name)
        # 计算d
        d = cal_d(y_predict, y_real, k)
        f = open(save_result_path + name + ".txt", "w")
        # f.writelines(str(target))       #写入一行即可
        f.writelines(str(y_predict) + '\n')
        f.writelines(str(y_real) + '\n')
        f.writelines(str(d))
        # f.write(d)
        f.close()
        return d

    # 计算y_predict
    def fun4(name1, name, check=True):  # name1: curve_3.txt  name = curve_3_mask.txt
        try:
            with open(y_data_path + name1, "r") as f:
                file = f.readlines()
                for line in file:
                    line = line.strip("\n")  # 去除末尾的换行符
                p = float(file[1])
                file[2] = file[2].strip('\n')
                y0_pixel = float(file[2])
                # print(y0_pixel)
                file[3] = file[3].strip('\n')
                y0 = int(file[3])
                # print(y0)
                # print("---------step1---------")
                # print(p)
                # print(y_data_path + name1)
                # print("基准值 = %d，基准值的pixel = %d" % (y0, y0_pixel))
                # print("---------step2：求y_predict---------")
            img = cv2.imread(data_path + "/check_test/" + name.split('.')[0] + ".png")
            y_predict, img = fun2(point_pixel_path + name, y0, y0_pixel, p, img)  # 算出来y_predict
            cv2.imwrite(data_path + "/check_test/" + name.split('.')[0] + ".png", img)
            # for y in y_predict:
            #     print(y)
            if check:
                return fun3(name, y_predict)
            else:
                return y_predict
        except:
            print("cannot find this txt ")

    point_pixel_path = data_path + "/point_pixel_txt/"
    y_data_path = data_path + "/Y_Data/"
    save_result_path = data_path + "/point_result/"

    # option = False
    option = True

    sum_d = 0

    if option:
        curvetups = []
        linetups = []
        for name in os.listdir(point_pixel_path):
            index = name.split('_')[1]
            if name.split('_')[0] == "curve":
                curvetups.append((int(index), name))
            else:
                linetups.append((int(index), name))

        curvetups.sort(key=lambda tup: tup[0])
        linetups.sort(key=lambda tup: tup[0])

        file = Workbook(encoding='utf-8')
        # 指定file以utf-8的格式打开
        sheet1 = file.add_sheet('curve')

        i = 0
        for curvetup in curvetups:
            y_predict = []
            data_list = []
            index, name = curvetup
            name1 = name.split('.')[0].split('_')[0] + '_' + name.split('.')[0].split('_')[1] + '.txt'
            print(name1)
            y_pre = fun4(name1, name, False)
            for j in range(0, 5):
                sheet1.write(i, j, y_pre[j])
            i += 1

        sheet2 = file.add_sheet('line')
        i = 0
        for linetup in linetups:
            y_predict = []
            data_list = []
            index, name = linetup
            name1 = name.split('.')[0].split('_')[0] + '_' + name.split('.')[0].split('_')[1] + '.txt'
            print(name1)
            y_pre = fun4(name1, name, False)
            for j in range(0, 5):
                sheet2.write(i, j, y_pre[j])
            i += 1

        file.save('test.xls')

    else:
        num = 0
        for name in os.listdir(point_pixel_path):
            name1 = name.split('.')[0].split('_')[0] + '_' + name.split('.')[0].split('_')[1] + '.txt'
            print(name1, name)
            y_predict = []
            data_list = []
            try:
                d_i = fun4(name1, name)  # name1 无mask
                sum_d += d_i
                num += 1
                print(d_i)
            except:
                print("error")
            # print(fun4(name1, name, False))
        print(sum_d / num)
