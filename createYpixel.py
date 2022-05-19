import os
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt


def getPixel(shape, x_pixel, raw_img, img_array, rec=True):
    y_pixel = []
    for i in range(0, shape[0]):  # shape[0] = 480
        value = img_array[i, x_pixel]
        if value > 0:
            # print("value %d" %value)
            y_pixel.append(i)

    num = len(y_pixel)
    sum0 = sum(y_pixel)

    if num != 0:
        avg = int(sum0 / num + 0.5)
        # print("sum = %d num = %d avg = %d" % (sum0, num, avg))
    else:
        y_pixel = []
        print(num)
        y_pixel, avg = getPixel(shape, x_pixel+1, raw_img, img_array, rec)

    if rec:
        cv2.rectangle(raw_img, (x_pixel, y_pixel[0]), (x_pixel + 1, y_pixel[0] + len(y_pixel)), (0, 0, 255), 1, 1,
                      0)

    return y_pixel, avg


# 该函数完成从mask图中，检测曲线上五个点的（x_pixel,y_pixel)

# 第一步，读取矩阵，找到最左边和最右边的x像素。
# 第二步 四等分，一起存到一个数组里面
# 第三步
# 转换二维数组的坐标值，改变图片颜色

# 搜索x轴的最左和最右，然后四等分
w = 0
h = 0


def fun4(name1):  # name1: curve_3.txt  name = curve_3_mask.txt
    try:
        # print(y_data_path + name1)
        with open(y_data_path + name1, "r") as f:
            file = f.readlines()
            for line in file:
                line = line.strip("\n")  # 去除末尾的换行符

            file[4].strip("\n")
            x_p = float(file[4])
        return x_p
    except:
        print("cannot find this txt ")


def fun1(img_path, savepath, name, imgname):

    raw_img = cv2.imread(data_path + "/images/" + imgname.split("_mask")[0] + '.png')
    name1 = name.split('.')[0].split('_')[0] + '_' + name.split('.')[0].split('_')[1] + '.txt'
    x_p = fun4(name1)

    img = Image.open(img_path)
    img_array = np.asarray(img)  # 把图像转成数组格式img = np.asarray(image)
    shape = img_array.shape
    # print(shape)

    x_pixel = []
    for i in range(0, shape[1]):  # shape[0]行总数  shape[1]是列总数
        for j in range(0, shape[0]):
            value = img_array[j, i]
            if value > 0:
                xmin = i
                x_pixel.append(i)  # 找最小
                break

        if len(x_pixel) == 1:
            break

    for i in range(shape[1] - 1, -1, -1):  # shape[0]行总数  shape[1]是列总数
        for j in range(0, shape[0]):
            value = img_array[j, i]
            if value > 0:
                x_pixel.append(i)
                xmax = i  # 找最大
                break
        if len(x_pixel) == 2:
            break
    try:
        a = (x_p + xmax - xmin) / 4
    except:
        a = (xmax - xmin) / 4
    tmp = xmin
    for i in range(0, 3):
        tmp = int(tmp + a + 0.5)
        x_pixel.append(tmp)  # 等分，四舍五入

    x_pixel.sort(reverse=False)
    # for x in x_pixel:
    #     print(x)
    # print("x_pixel类列表的长度为%d" % len(x_pixel))

    # print("遍历像素矩阵，找到对应的一系列y轴像素值")
    # 遍历像素矩阵，找到对应的一系列y轴像素值。w = 480，h = 640
    target = []
    for k in range(0, len(x_pixel)):  # 五个x_pixel值，
        y_pixel, avg = getPixel(shape, x_pixel[k], raw_img, img_array)
        y_p_out = avg

        if k == 0:
            y_pixel1, avg1 = getPixel(shape, x_pixel[k] + 1, raw_img, img_array, False)
            if avg1 - avg < 0:
                y_p_out = y_pixel[len(y_pixel) - 1]
            if avg1 - avg > 0:
                y_p_out = y_pixel[0]
        elif k == len(x_pixel) - 1:
            y_pixel1, avg1 = getPixel(shape, x_pixel[k] - 1, raw_img, img_array, False)
            if avg - avg1 < 0:
                y_p_out = y_pixel[0]
            if avg - avg1 > 0:
                y_p_out = y_pixel[len(y_pixel) - 1]
        elif True:
            y_pixel1, avg1 = getPixel(shape, x_pixel[k] + 1, raw_img, img_array, False)
            if avg1 - avg < 0:
                y_p_out = y_pixel[len(y_pixel) - 1]
            if avg1 - avg > 0:
                y_p_out = y_pixel[0]
        # elif len(y_pixel) > 25:
        #     y_pixel1, avg1 = getPixel(shape, x_pixel[k] + 1, raw_img, img_array, False)
        #     if avg1 - avg < 0:
        #         y_p_out = y_pixel[len(y_pixel) - 1]
        #     if avg1 - avg > 0:
        #         y_p_out = y_pixel[0]

        target.append((x_pixel[k], y_p_out))
    cv2.imwrite(save_image + imgname, raw_img)

    f = open(savepath + name + ".txt", "w")
    # f.writelines(str(target))       #写入一行即可
    for t in target:
        string = str(t)
        content = string.split('(')[1].split(')')[0]
        f.write(content + '\n')
    f.close()


# data_path = "/media/queahren/DATA/MYDATA"
# image_path = data_path + '/1st_manual/'
# save_txt = data_path + '/point_pixel_txt/'
# save_image = data_path + "/check_test/"
# y_data_path = data_path + "/Y_Data/"
# data_path = "/media/queahren/DATA/testData/测试数据"
data_path = "/media/queahren/DATA/DATA_A28_same"
image_path = data_path + '/result/'
save_txt = data_path + '/point_pixel_txt/'
save_image = data_path + "/check_test/"
y_data_path = data_path + "/Y_Data/"


for img in os.listdir(image_path):
    if (img.endswith('.png')):
        name = img.split('.')[0]
        print(name)
        fun1(image_path + img, save_txt, name, img)

# fun1('/Users/jsy/Desktop/curve_0_mask.png' , save_txt_path)
