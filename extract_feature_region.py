import math

import cv2 as cv
import numpy as np
import os
from scipy import spatial

src_dic = "duiqi1" # 图像文件夹

images_list = os.listdir(src_dic)

def detect_IR_circle(cimage):
    hollow_coord = []

    circles = cv.HoughCircles(cimage, cv.HOUGH_GRADIENT, 1, 20, param1=300, param2=10, minRadius=0, maxRadius=15)
    circles = np.uint16(np.around(circles))  # 把circles包含的圆心和半径的值变成整数
    circles = np.squeeze(circles)
    # print(circles.shape[1])
    dst_circles1 = []
    dst_circles2 = []
    dst_circles3 = []


    for i in range(len(circles)):
        if cimage[circles[i][1] - 1, circles[i][0] - 1] < 130:
            pass
        else:
            dst_circles1.append(circles[i, :])

    if len(dst_circles1) == 4:
        dst_circles2 = dst_circles1
    else:
        for i in dst_circles1[:]:
            if i[1] > 200 and i[0] > 200 and i[1] < cimage.shape[0] * 0.9 and i[0] < cimage.shape[1] * 0.9:
                dst_circles2.append(i[:])
            else:
                pass

    if len(dst_circles2)== 5:
        data = np.array(dst_circles2)
        idex = np.lexsort([data[:, 0]])
        sorted_data = data[idex, :]
        sorted_data1 = sorted_data[0:3]

        idex1 = np.lexsort([sorted_data1[:, 1]])
        sorted_data2 = sorted_data1[idex1, :]
        to_del = sorted_data2[1]

        for i in dst_circles2[:]:
            if i[0]==to_del[0] and i[1]==to_del[1] and i[2]==to_del[2]:
                pass
            else:
                dst_circles3.append(i[:])
        hollow_coord = dst_circles3[:]
    elif len(dst_circles2) == 4:
        for i in dst_circles2[:]:
            hollow_coord.append(i[:])
    elif len(dst_circles2) == 6:
        arr_dst_circles2 = np.array(dst_circles2)
        dst_matrix = spatial.distance_matrix(arr_dst_circles2, arr_dst_circles2)
        min_dst = 99999
        index_i = 0
        index_y = 0
        for i in range(dst_matrix.shape[0]):
            for j in range(dst_matrix.shape[1]):
                if dst_matrix[i][j] == 0:
                    pass
                elif dst_matrix[i][j] < min_dst:
                    index_i = i
                    index_y = j
                    min_dst = dst_matrix[i][j]
                else:
                    pass

        for k in range(6):
            if k == index_y or k == index_i:
                pass
            else:
                hollow_coord.append(dst_circles2[k][:])

    else:
        print("ERROR")


    return hollow_coord

def detect_RGB_circle(cimage):
    hollow_coord = []

    circles = cv.HoughCircles(cimage, cv.HOUGH_GRADIENT, 5, 70, param1=300, param2=60, minRadius=0, maxRadius=30)
    circles = np.uint16(np.around(circles))  # 把circles包含的圆心和半径的值变成整数
    circles = np.squeeze(circles)

    dst_circles1 = []

    for i in range(len(circles)):

        if cimage[circles[i][1] - 1, circles[i][0] - 1] < 150:
            pass
        else:
            dst_circles1.append(circles[i])

    dst_circles2 = []
    if len(dst_circles1) == 4:
        dst_circles2 = dst_circles1
    else:
        for i in range(len(dst_circles1)):
            if dst_circles1[i][0] >= 500 and dst_circles1[i][1] >= 500 and dst_circles1[i][1] <= cimage.shape[0] * 0.9 and dst_circles1[i][0] <= cimage.shape[1] * 0.9:
                dst_circles2.append(dst_circles1[i][:])
            else:
                pass

    if len(dst_circles2) == 5:
        dst_circles3 = []
        data = np.array(dst_circles2)
        idex = np.lexsort([data[:, 0]])
        sorted_data = data[idex, :]
        sorted_data1 = sorted_data[0:3]

        idex1 = np.lexsort([sorted_data1[:, 1]])
        sorted_data2 = sorted_data1[idex1, :]
        to_del = sorted_data2[1]

        for i in dst_circles2[:]:
            if i[0] == to_del[0] and i[1] == to_del[1] and i[2] == to_del[2]:
                pass
            else:
                dst_circles3.append(i[:])
        hollow_coord = dst_circles3
    elif len(dst_circles2) == 6:
        arr_dst_circles2 = np.array(dst_circles2)
        dst_matrix = spatial.distance_matrix(arr_dst_circles2, arr_dst_circles2)
        min_dst = 99999
        index_i = 0
        index_y = 0
        for i in range(dst_matrix.shape[0]):
            for j in range(dst_matrix.shape[1]):
                if dst_matrix[i][j] == 0:
                    pass
                elif dst_matrix[i][j] < min_dst:
                    index_i = i
                    index_y = j
                    min_dst = dst_matrix[i][j]
                else:
                    pass

        for k in range(6):
            if k == index_y or k == index_i:
                pass
            else:
                hollow_coord.append(dst_circles2[k][:])

    elif len(dst_circles2) == 4:
        for i in dst_circles2[:]:
            hollow_coord.append(i[:])

    else:
        print("ERROR")

    return hollow_coord

def sort_coord(coordinate):
    coordinate_data = np.array(coordinate)
    index_x = np.lexsort([coordinate_data[:, 0]])
    sorted_x = coordinate_data[index_x, :]
    index_y = np.lexsort([coordinate_data[:, 1]])
    sorted_y = coordinate_data[index_y, :]
    left_points = sorted_x[0:2]
    left_y = np.lexsort([left_points[:, 1]])
    top_left = [left_points[left_y, :][0][0]+2*left_points[left_y, :][0][2], left_points[left_y, :][0][1]+2*left_points[left_y, :][0][2]]
    bottom_left = [left_points[left_y, :][1][0]+2*left_points[left_y, :][1][2], left_points[left_y, :][1][1]-2*left_points[left_y, :][1][2]]

    right_points = sorted_x[2:]
    right_y = np.lexsort([right_points[:, 1]])
    top_right = [right_points[right_y, :][0][0]-2*right_points[right_y, :][0][2], right_points[right_y, :][0][1]+2*right_points[right_y, :][0][2]]
    bottom_right = [right_points[right_y, :][1][0]-2*right_points[right_y, :][1][2], right_points[right_y, :][1][1]-2*right_points[right_y, :][1][2]]

    sorted_coordinate = [top_left, bottom_left, bottom_right, top_right]
    sorted_coordinate1 = np.array(sorted_coordinate)
    index_x1 = np.lexsort([sorted_coordinate1[:, 0]])
    sorted_x1 = sorted_coordinate1[index_x1, :]
    index_y1 = np.lexsort([sorted_coordinate1[:, 1]])
    sorted_y1 = sorted_coordinate1[index_y1, :]
    outer_bounds = [sorted_x1[0][0], sorted_y1[0][1], sorted_x1[-1][0], sorted_y1[-1][1]]
    inner_bounds = [sorted_x1[1][0], sorted_y1[1][1], sorted_x1[-2][0], sorted_y1[-2][1]]
    return sorted_coordinate, outer_bounds, inner_bounds

def cal_angle(point_1, point_2, point_3):
    a = math.sqrt(abs(point_2[0]-point_3[0])**2 + abs(point_2[1]-point_3[1])**2)
    b = math.sqrt(abs(point_1[0]-point_3[0])**2 + abs(point_1[1]-point_3[1])**2)
    c = math.sqrt(abs(point_2[0]-point_1[0])**2 + abs(point_2[1]-point_1[1])**2)
    angle_c = math.degrees(math.acos((c * c - a * a - b * b) / (-2 * a * b)))

    return angle_c

def isRayIntersects(poi, s_poi, e_poi):
    line0_a = float(poi[1])

    line0_b = float(- poi[0])

    line0_c = 0

    line1_a = float(s_poi[1]) - float(e_poi[1])

    line1_b = float(e_poi[0]) - float(s_poi[0])

    line1_c = float(s_poi[0]) * float(e_poi[1]) - float(e_poi[0]) * float(s_poi[1])

    d = float(line0_a * line1_b) - float(line1_a * line0_b)

    if d == 0:
        # 重合的边线没有交点

        return None

    x = float((line0_b * line1_c - line1_b * line0_c) * 1.0 / d)

    y = float((line0_c * line1_a - line1_c * line0_a) * 1.0 / d)

    pt = [x, y]

    if (pt[0] - poi[0]) * (pt[0]) <= 0 and (pt[0] - s_poi[0]) * (pt[0] - e_poi[0]) <= 0:

        # 判断交点是否在两条线段上

        return pt

    else:

        # 交点不在两条线段上除外

        return None

def isRayIntersectsSegment(poi, point1, point2, point3, point4):

    intersect1 = isRayIntersects(poi, point2, point1)
    intersect2 = isRayIntersects(poi, point4, point1)

    intersect3 = isRayIntersects(poi, point2, point3)
    intersect4 = isRayIntersects(poi, point4, point3)

    if intersect1 == None and intersect2 == None and intersect3 == None and intersect4 == None:
        return False
    else:
        if intersect3 == None and intersect4 ==None and (intersect1 !=None or intersect2 != None):
            inter_points = 1
            return True
        elif (intersect3 != None or intersect4 != None) and (intersect2 != None or intersect1 != None):
            inter_points = 2
            return False

def is_point_in_rect(sorted_coord, point):
    # polylen = len(sorted_coord)
    # sinsc = 0  # 交点个数
    # for i in range(polylen):
    #     if i == 0:
    #         s_poi = sorted_coord[i]
    #         e_poi = sorted_coord[i + 1]
    #         if isRayIntersectsSegment(point, [0, 0], s_poi, e_poi):
    #             sinsc += 1
    #     elif i == 3:
    #         s_poi = sorted_coord[i]
    #         e_poi = sorted_coord[0]
    #         if isRayIntersectsSegment(point, [0, 0], s_poi, e_poi):
    #             sinsc += 1
    #     else:
    #         pass
    if isRayIntersectsSegment(point, sorted_coord[0], sorted_coord[1], sorted_coord[2], sorted_coord[3]):
        return True
    else:
        return False
    # return True if sinsc % 2 == 1 else False

def image_clip(image, coordinate, add_name):
    sorted_coord, outer_bounds, inner_bounds = sort_coord(coordinate)
    new_image = image.copy()

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if i <= outer_bounds[1] or i >= outer_bounds[3] or j <= outer_bounds[0] or j >= outer_bounds[2]:
                new_image[i][j][:] = 255
            elif i >= inner_bounds[1] and i <= inner_bounds[3] and j >= inner_bounds[0] and j <= inner_bounds[2]:
                pass
            else:
                point_in_rect = is_point_in_rect(sorted_coord, [j, i])
                if (point_in_rect == False):
                    new_image[i][j][:] = 255
                else:
                    pass

    # cv.rectangle(new_image, (outer_bounds[0], outer_bounds[1]), (outer_bounds[2], outer_bounds[3]), (0, 0, 255), 2)
    # cv.rectangle(new_image, (inner_bounds[0], inner_bounds[1]), (inner_bounds[2], inner_bounds[3]), (0, 255, 0), 2)
    # for i in range(4):
    #     if i != 3:
    #         cv.line(new_image, (sorted_coord[i][0], sorted_coord[i][1]), (sorted_coord[i+1][0], sorted_coord[i+1][1]), (255, 0, 0), 2)
    #     else:
    #         cv.line(new_image, (sorted_coord[i][0], sorted_coord[i][1]), (sorted_coord[0][0], sorted_coord[0][1]), (255, 0, 0), 2)

    new_name = 'result_duiqi1/'+add_name.split('.jpg')[0]+'_cliped1'+'.jpg'
    cv.imwrite(new_name, new_image)
    print("%s has been saved!" % new_name)

for image_name in images_list:
    image = cv.imread(os.path.join(src_dic, image_name))
    dst = cv.pyrMeanShiftFiltering(image, 10, 100)  # 边缘保留滤波EPF
    cimage = cv.cvtColor(dst, cv.COLOR_RGB2GRAY)
    if image_name.split('.')[1] == 'jpg':
        if 'IR' in image_name.split('.')[0]:
            print("Processing IR image %s" % image_name)
            hollow_coord = detect_IR_circle(cimage)
            image_clip(image, hollow_coord, image_name)
        elif 'RGB' in image_name.split('.')[0]:
            print("Processing RGB image %s" % image_name)
            hollow_coord = detect_RGB_circle(cimage)
            image_clip(image, hollow_coord, image_name)
    else:
        pass
