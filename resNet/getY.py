def getY(new_rects):
    # print(new_rects)
    new_rects.sort(key=lambda tup: tup[0])  # sorts in place 原地排序
    # print(new_rects)
    # 提取Y轴
    rects_y = []
    for index in range(len(new_rects)):
        rects_y.append(new_rects[index])
        #     print(new_rects[index+1][0] - new_rects[index][0])
        if new_rects[index + 1][0] - new_rects[index][0] - new_rects[index][2] > 4:
            break
    # print(rects_y)
    rects_y.sort(key=lambda tup: tup[1])
    # print(rects_y)

    rects_y_num = []
    rect_y_num = []

    for index in range(0, len(rects_y) - 1):
        rect_y_num.append(rects_y[index])
        if rects_y[index + 1][0] - rects_y[index][0] - rects_y[index][2] > 3 or rects_y[index + 1][1] - rects_y[index][1] > 2:
            rects_y_num.append(rect_y_num)
            rect_y_num = []
    rect_y_num.append(rects_y[len(rects_y) - 1])
    rects_y_num.append(rect_y_num)
    # print(rects_y_num)

    y_nums = []
    for rect_y_num in rects_y_num:
        rect_y_num.sort(key=lambda tup: tup[0], reverse=True)
        y_num = 0
        y_pic = 0
        for i in range(0, len(rect_y_num)):
            y_num += rect_y_num[i][4] * pow(10, i)
            y_pic += (2 * rect_y_num[i][1] + rect_y_num[i][3]) / 2
        y_nums.append((y_num, y_pic / len(rect_y_num)))
    # print(y_nums)

    return y_nums
