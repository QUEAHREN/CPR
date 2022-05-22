import os
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt


def createYpixel(data_path):
    def getPixel(shape, x_pixel, raw_img, img_array, gray_img_array, rec=True, k=1):
        y_pixel = []

        gray_y = []
        for i in range(0, shape[0]):  # shape[0] = 480
            value = img_array[i, x_pixel]
            if value > 0:
                # print("value %d" %value)
                y_pixel.append(i)
                gray_y.append(gray_img_array[i, x_pixel])

        num = len(y_pixel)
        sum0 = sum(y_pixel)

        if num != 0:
            avg = int(sum0 / num + 0.5)
            gray_avg = int(sum(gray_y) / num + 0.5)

            up_cnt = 0
            up_y_pixel = y_pixel[0]
            for i in range(0, num - 1):
                if gray_y[i] > gray_avg:
                    up_cnt += 1
                else:
                    up_y_pixel = y_pixel[i]
                    break

            down_cnt = 0
            down_y_pixel = y_pixel[num - 1]
            for i in range(num - 1, 0, -1):
                if gray_y[i] > gray_avg:
                    down_cnt += 1
                else:
                    down_y_pixel = y_pixel[i]
                    break

            if up_cnt < down_cnt:
                best_y = up_y_pixel
            elif down_cnt < up_cnt:
                best_y = down_y_pixel
            else:
                best_y = int((up_y_pixel + down_y_pixel) / 2)
            if abs(up_cnt - down_cnt) / num <= 0.12:
                best_y = int((up_y_pixel + down_y_pixel) / 2)

            print(gray_y)
            print(y_pixel)
            # print("sum = %d num = %d avg = %d" % (sum0, num, avg))
        else:
            y_pixel = []
            print(num)
            if k > 0:
                best_y, y_pixel, avg = getPixel(shape, x_pixel + k, raw_img, img_array, gray_img_array, rec, -1 * k)
            else:
                best_y, y_pixel, avg = getPixel(shape, x_pixel + k, raw_img, img_array, gray_img_array, rec, -(k - 1))

            # y_pixel, avg = getPixel(shape, x_pixel + 1, raw_img, img_array, rec)
        if rec:
            cv2.rectangle(raw_img, (x_pixel - 1, y_pixel[0] - 1), (x_pixel + 1, y_pixel[0] + len(y_pixel) + 1),
                          (0, 0, 255),
                          1, 1,
                          0)

        return best_y, y_pixel, avg

    w = 0
    h = 0

    def fun4(name1):  # name1: curve_3.txt  name = curve_3_mask.txt
        try:
            # print(y_data_path + name1)
            with open(y_data_path + name1, "r") as f:
                file = f.readlines()
                for line in file:
                    line = line.strip("\n")  # 去除末尾的换行符
                file[0].strip("\n")
                file[0] = file[0].split(")")[0]
                file[0] = file[0].split("(")[1]
                x0 = int(file[0].split(",")[0])
                x0_pixel = float(file[0].split(",")[1])

                file[4].strip("\n")
                x_p = float(file[4])
                print(x0_pixel)
            return x_p, x0, x0_pixel
        except:
            print("cannot find this txt ")

    def fun1(img_path, savepath, name, imgname):
        raw_img = cv2.imread(data_path + "/images/" + imgname.split("_mask")[0] + '.png')
        gray_img = Image.open(data_path + "/gray/" + imgname.split("_mask")[0] + '.png')
        gray_img_array = np.asarray(gray_img)

        name1 = name.split('.')[0].split('_')[0] + '_' + name.split('.')[0].split('_')[1] + '.txt'
        x_p, x0, x0_pixel = fun4(name1)

        img = Image.open(img_path)
        img_array = np.asarray(img)  # 把图像转成数组格式img = np.asarray(image)
        shape = img_array.shape
        # print(shape)

        x_pixel = []
        xmin = 0
        for i in range(0, shape[1]):  # shape[0]行总数  shape[1]是列总数
            for j in range(0, shape[0]):
                value = img_array[j, i]
                if value > 0:
                    xmin = i
                    break
            if xmin != 0:
                break

        if abs(x0_pixel - xmin) > 6:
            xmin = int(x0_pixel + 0.5)
        x_pixel.append(xmin)
        # print(xmin)

        for i in range(shape[1] - 1, -1, -1):  # shape[0]行总数  shape[1]是列总数
            for j in range(0, shape[0]):
                value = img_array[j, i]
                if value > 0:
                    x_pixel.append(i)
                    xmax = i  # 找最大
                    break
            if len(x_pixel) == 2:
                break

        a = (x_p + xmax - xmin) / 4

        tmp = xmin

        for i in range(0, 3):
            x_pixel.append(int(tmp + a))  # 等分，四舍五入
            tmp = tmp + a

        x_pixel.sort(reverse=False)
        # print(x_pixel)
        # print("x_pixel类列表的长度为%d" % len(x_pixel))

        # print("遍历像素矩阵，找到对应的一系列y轴像素值")
        # 遍历像素矩阵，找到对应的一系列y轴像素值。w = 480，h = 640
        target = []
        for k in range(0, len(x_pixel)):  # 五个x_pixel值，

            print(k)
            best_y, y_pixel, avg = getPixel(shape, x_pixel[k], raw_img, img_array, gray_img_array)
            y_p_out = best_y
            if k == 0:
                best_y1, y_pixel1, avg1 = getPixel(shape, x_pixel[k] + 1, raw_img, img_array, gray_img_array, False)
                if avg1 - avg <= 0:
                    y_p_out = y_pixel[len(y_pixel) - 1]
                if avg1 - avg > 0:
                    y_p_out = y_pixel[0]
            elif k == len(x_pixel) - 1:
                best_y1, y_pixel1, avg1 = getPixel(shape, x_pixel[k] - 1, raw_img, img_array, gray_img_array, False)
                if avg - avg1 <= 0:
                    y_p_out = y_pixel[0]
                if avg - avg1 > 0:
                    y_p_out = y_pixel[len(y_pixel) - 1]

            target.append((x_pixel[k], y_p_out))

        cv2.imwrite(save_image + imgname, raw_img)

        f = open(savepath + name + ".txt", "w")
        # f.writelines(str(target))       #写入一行即可
        for t in target:
            string = str(t)
            content = string.split('(')[1].split(')')[0]
            f.write(content + '\n')
        f.close()

    image_path = data_path + '/mergeResult/'
    save_txt = data_path + '/point_pixel_txt/'
    save_image = data_path + "/check_test/"
    y_data_path = data_path + "/Y_Data/"

    if not os.path.exists(save_txt):
        os.mkdir(save_txt)
    if not os.path.exists(save_image):
        os.mkdir(save_image)

    pictups = []
    for name in os.listdir(image_path):
        index = name.split('_')[1]
        # if name.split('_')[0] == "curve":
        pictups.append((int(index), name))

    pictups.sort(key=lambda tup: tup[0])

    for index, img in pictups:
        if img.endswith('.png'):
            name = img.split('.')[0]
            print(name)
            fun1(image_path + img, save_txt, name, img)

    # for img in os.listdir(image_path):
    #     if (img.endswith('.png')):
    #         name = img.split('.')[0]
    #         print(name)
    #         fun1(image_path + img, save_txt, name, img)

    # fun1('/Users/jsy/Desktop/curve_0_mask.png' , save_txt_path)
