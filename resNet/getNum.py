import cv2
import os
from matplotlib import pyplot as plt
from .predict import *
from .getX import getX
from .getY import getY
from .resize import resize
from PIL import Image, ImageDraw


def predImage(img_path):
    assert os.path.exists(img_path), "file: '{}' dose not exist.".format(img_path)
    img = Image.open(img_path)
    return predict(img)


# 不算最后一个数据
def calP(y_nums):
    y_nums.sort(key=lambda tup: tup[0], reverse=True)
    if len(y_nums) > 2:
        dy = y_nums[0][0] - y_nums[len(y_nums) - 2][0]
        dy_p = y_nums[0][1] - y_nums[len(y_nums) - 2][1]
        p = dy / dy_p
    elif len(y_nums) == 2:
        dy = y_nums[0][0] - y_nums[1][0]
        dy_p = y_nums[0][1] - y_nums[1][1]
        p = dy / dy_p
    else:
        print("error")
    return p, y_nums[0]


def getNum(data_path):
    # data_path = "/media/queahren/DATA/DATA_A28_same"
    img_path = data_path + "/images"
    filename = os.listdir(img_path)
    base_dir = img_path + "/"
    font = cv2.FONT_HERSHEY_SIMPLEX

    save_path_nums = data_path + "/nums/"
    save_path_data = data_path + "/Y_Data/"
    save_path_preview = data_path + "/preview/"

    if not os.path.exists(save_path_nums):
        os.mkdir(save_path_nums)
    if not os.path.exists(save_path_data):
        os.mkdir(save_path_data)
    if not os.path.exists(save_path_preview):
        os.mkdir(save_path_preview)
    for imgname in filename:
        if imgname.endswith('.png'):

            print(imgname)

            img = cv2.imread(base_dir + imgname)
            gray = cv2.imread(base_dir + imgname, cv2.IMREAD_GRAYSCALE)

            mean, std = cv2.meanStdDev(gray)
            if mean < 50:
                gray = 255 - gray

            bw = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 25)
            img2, ctrs, hier = cv2.findContours(
                bw.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            rects = [cv2.boundingRect(ctr) for ctr in ctrs]

            save_path = save_path_nums + imgname.split('.')[0] + '/'

            if not os.path.exists(save_path):
                os.mkdir(save_path)

            file0 = open(save_path_data + imgname.split('.')[0] + ".txt", 'w+')
            new_rects = []
            i = 0

            for rect in rects:

                x, y, w, h = rect
                roi = gray[y:y + h, x:x + w]
                #         print(w,h)
                if w > 4 and 20 > h > 5:
                    #             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 1, 1, 0);
                    if w / h >= 1 and w < 22:
                        res = cv2.resize(roi, (2 * w, 2 * h))
                        res1 = resize(res[0:2 * h, 0:w])
                        res2 = resize(res[0:2 * h, w:2 * w])

                        cv2.imwrite(save_path + '%d.jpg' % i, (res1))
                        num, prob = predImage(save_path + '%d.jpg' % i)
                        new_rects.append((x, y, round(w / 2), h, num, i))
                        cv2.rectangle(img, (x, y), (x + round(w / 2), y + h), (0, 0, 255), 1, 1, 0);
                        cv2.putText(img, '{:.0f}'.format(num), (x, y), cv2.FONT_HERSHEY_DUPLEX, h / 25.0, (255, 0, 0))
                        i += 1

                        cv2.imwrite(save_path + '%d.jpg' % i, (res2))
                        num, prob = predImage(save_path + '%d.jpg' % i)
                        new_rects.append((x + round(w / 2), y, round(w / 2), h, num, i))
                        cv2.rectangle(img, (x + round(w / 2), y), (x + w, y + h), (0, 0, 255), 1, 1, 0);
                        cv2.putText(img, '{:.0f}'.format(num), (x + round(w / 2), y), cv2.FONT_HERSHEY_DUPLEX, h / 25.0,
                                    (255, 0, 0))
                        i += 1

                    elif w < 15:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1, 1, 0);
                        res = resize(roi)
                        cv2.imwrite(save_path + '%d.jpg' % i, res)
                        num, prob = predImage(save_path + '%d.jpg' % i)
                        rect += tuple((num, i))
                        new_rects.append(rect)
                        cv2.putText(img, '{:.0f}'.format(num), (x, y), cv2.FONT_HERSHEY_DUPLEX, h / 25.0, (255, 0, 0))
                        i += 1

            cv2.imwrite(save_path_preview + imgname, img)
            y_nums = getY(new_rects)
            p, y_num_max = calP(y_nums)
            y_nums, x_p = getX(new_rects)
            print(y_nums, file=file0)
            print(p, file=file0)
            print(y_num_max[1], file=file0)
            print(y_num_max[0], file=file0)
            print(x_p, file=file0)
            file0.close()
