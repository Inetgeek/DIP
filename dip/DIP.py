#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
 @author: Colyn
 @project: digital_img_processing
 @devtool: PyCharm
 @date: 2023/3/28
 @file: DIP.py
"""

import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def plt_line(X, Y, save_path):
    """
    绘制图像的对比度折线图
    :param X: 点的横坐标
    :param Y: 点的纵坐标
    :param save_path: 图片保存位置
    :return: None
    """
    plt.figure(figsize=(5, 5), dpi=300)
    plt.plot(X, Y, marker='o', markersize=5, markeredgecolor="red", markerfacecolor="red")
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.2)
    plt.clf()


def plt_hist(img, save_path):
    """
    绘制图像的灰度直方图
    :param img: 输入的图像
    :param save_path: 图片保存位置
    :return: None
    """
    plt.figure(figsize=(5, 5), dpi=300)
    ar = img[:, :, 0].flatten()
    plt.hist(ar, bins=256, density=1, facecolor='r', edgecolor='r')
    ag = img[:, :, 1].flatten()
    plt.hist(ag, bins=256, density=1, facecolor='g', edgecolor='g')
    ab = img[:, :, 2].flatten()
    plt.hist(ab, bins=256, density=1, facecolor='b', edgecolor='b')
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.2)
    plt.clf()


def plt_imgs(img, save_path):
    """
    绘制图片背景图
    :param img: 输入的图片
    :param save_path: 图片保存位置
    :return: None
    """
    plt.figure(figsize=(5, 5), dpi=300)
    plt.axis('off')
    plt.imshow(img[:, :, ::-1], cmap='gray', vmin=0, vmax=255)
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.2)
    plt.clf()


def linear_stretch(img, x1, x2, y1, y2):
    """
    分段线性变换API
    :param img: 输入的图片
    :param x1: 点A的横坐标
    :param x2: 点B的横坐标
    :param y1: 点A的纵坐标
    :param y2: 点B的纵坐标
    :return: None
    """
    lut = np.zeros(256)
    for i in range(256):
        if i < x1:
            lut[i] = (y1 / x1) * i
        elif i < x2:
            lut[i] = ((y2 - y1) / (x2 - x1)) * (i - x1) + y1
        else:
            lut[i] = ((y2 - 255.0) / (x2 - 255.0)) * (i - 255.0) + 255.0
    img_output = cv.LUT(img, lut)
    img_output = np.uint8(img_output + 0.5)
    return img_output


class DIP(object):
    """
    数字图像处理，用于处理RGB彩色图像的分段线性拉伸变换的算法
    """

    def __init__(self, img_path: str, output_dir: str, x1: int = 0, x2: int = 255, y1: int = 0, y2: int = 255):
        assert 0 <= x1 <= 255, "The value of x1 must be between 0 and 255 !"
        assert 0 <= x2 <= 255, "The value of x2 must be between 0 and 255 !"
        assert 0 <= y1 <= 255, "The value of y1 must be between 0 and 255 !"
        assert 0 <= y2 <= 255, "The value of y2 must be between 0 and 255 !"
        assert x1 <= x2, "The value of x1 must be lower than x2 !"
        assert y1 <= y2, "The value of y1 must be lower than y2 !"
        self.init_img = img_path
        self.X1 = x1
        self.X2 = x2
        self.Y1 = y1
        self.Y2 = y2
        self.output = output_dir
        self.list_X = [0, self.X1, self.X2, 255]
        self.list_Y = [0, self.Y1, self.Y2, 255]
        os.makedirs(os.path.join('.', self.output), exist_ok=True)

    def is_exist(self):
        """
        判断文件是否存在
        :return: boolean, 存在则为True, 不存在则为False
        """
        return os.path.isfile(self.init_img)

    def get_init_img(self):
        """
        获取原始图片的背景图、对比度折线图及RGB灰度直方图
        :return: img_init, img_line, img_hist
        """
        img = cv.imread(self.init_img).astype(np.uint8)
        img_init = f'./{self.output}/init_img.png'
        img_line = f'./{self.output}/init_line.png'
        img_hist = f'./{self.output}/init_hist.png'
        plt_line(self.list_X, self.list_Y, img_line)
        plt_hist(img, img_hist)
        plt_imgs(img, img_init)

        return img_init, img_line, img_hist

    def get_dips_img(self, x1: int = 0, x2: int = 255, y1: int = 0, y2: int = 255):
        """
        获取处理后图片的背景图、对比度折线图及RGB灰度直方图
        :param x1: 点A的横坐标
        :param x2: 点B的横坐标
        :param y1: 点A的纵坐标
        :param y2: 点B的纵坐标
        :return: img_init, img_line, img_hist
        """
        assert 0 <= x1 <= 255, "The value of x1 must be between 0 and 255 !"
        assert 0 <= x2 <= 255, "The value of x2 must be between 0 and 255 !"
        assert 0 <= y1 <= 255, "The value of y1 must be between 0 and 255 !"
        assert 0 <= y2 <= 255, "The value of y2 must be between 0 and 255 !"
        assert x1 <= x2, "The value of x1 must be lower than x2 !"
        assert y1 <= y2, "The value of y1 must be lower than y2 !"
        img_i = cv.imread(self.init_img).astype(np.uint8)
        img_d = linear_stretch(img_i, x1, x2, y1, y2)
        img_init = f'./{self.output}/dips_img.png'
        img_line = f'./{self.output}/dips_line.png'
        img_hist = f'./{self.output}/dips_hist.png'
        self.list_X[1] = x1
        self.list_X[2] = x2
        self.list_Y[1] = y1
        self.list_Y[2] = y2
        plt_line(self.list_X, self.list_Y, img_line)
        plt_hist(img_d, img_hist)
        plt_imgs(img_d, img_init)

        return img_init, img_line, img_hist

    def get_cmp_plot(self, *args, **kwargs):
        """
        绘制处理前后的图片本身、对比折线图及灰度直方图
        :param args: 需要显示的图片路径
        :param kwargs: 设置需要显示的图片标题
        :return: None
        """
        length, skip, list_img, cnt = len(args), -1, [], 0
        if type(args[0]).__name__ == "DIP":
            length -= 1
            skip = 0

        for i in args:
            if skip == args.index(i):
                continue
            assert os.path.exists(f'{i}'), f"The {i} is not exist!"
            list_img.append(i)
        width = 3
        height = (length // 3 + 1) if length % 3 else (length // 3)
        title = [_ for _ in kwargs]
        plt.figure(figsize=(width * 5, height * 5), dpi=300)
        img = [cv.imread(im).astype(np.uint8) for im in list_img]
        for im in img:
            plt.subplot(height, width, (cnt + 1)), plt.imshow(im[:, :, ::-1], cmap='gray', vmin=0, vmax=255), plt.title(kwargs[title[cnt]])
            plt.axis('off')
            cnt += 1
        plt.tight_layout()
        plt.savefig(f"./{self.output}/cmp.png", bbox_inches='tight', pad_inches=0.2)
        plt.show()
        plt.clf()
