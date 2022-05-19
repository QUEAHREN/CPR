def getX(new_rects):

    new_rects.sort(key=lambda tup: tup[1], reverse=True)  # sorts in place 原地排序
    # 提取X轴
    rects_x = []
    for index in range(len(new_rects)):
        rects_x.append(new_rects[index])
        #     print(new_rects[index+1][0] - new_rects[index][0])
        if abs(new_rects[index + 1][1] - new_rects[index][1]) > 4:
            break

    rects_x.sort(key=lambda tup: tup[0])

    rects_x_num = []
    rect_x_num = []

    for index in range(0, len(rects_x) - 1):
        rect_x_num.append(rects_x[index])
        if (rects_x[index + 1][0] - rects_x[index][0] - rects_x[index][2] > 3 or rects_x[index + 1][1] - rects_x[index][
            1] > 2):
            rects_x_num.append(rect_x_num)
            rect_x_num = []
    rect_x_num.append(rects_x[len(rects_x) - 1])
    rects_x_num.append(rect_x_num)

    # 提取X轴测试文件
    x_nums = []
    for rect_x_num in rects_x_num:
        rect_x_num.sort(key=lambda tup: tup[0], reverse=True)
        x_num = 0
        x_pic = 0
        for i in range(0, len(rect_x_num)):
            x_num += rect_x_num[i][4] * pow(10, i)
            x_pic += (2 * rect_x_num[i][0] + rect_x_num[i][2]) / 2
        x_nums.append((x_num, x_pic / len(rect_x_num)))

    x_nums.sort(key=lambda tup: tup[0])
    x_p = (x_nums[len(x_nums)-1][1] - x_nums[0][1]) / (x_nums[len(x_nums)-1][0] - x_nums[0][0])

    return x_nums, x_p
