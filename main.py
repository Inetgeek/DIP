#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
 @author: Colyn
 @project: digital_img_processing
 @devtool: PyCharm
 @date: 2023/3/28
 @file: main.py
"""
from dip.DIP import DIP
from dip import log as l

if __name__ == '__main__':
    print("==" * 10, "DEMO", "==" * 10)
    log = l.Log(name='log.txt', log_level=l.logging.DEBUG)

    dip = DIP(img_path="./pic/2.png", output_dir="data")
    log.debug(f"Is the image exist? [{dip.is_exist()}]")

    init_img, init_line, init_hist = dip.get_init_img()
    log.info(f"The initial image is in: {init_img}")
    log.info(f"The initial line is in: {init_line}")
    log.info(f"The initial hist is in: {init_hist}")

    dips_img, dips_line, dips_hist = dip.get_dips_img(x1=120, x2=240, y1=250, y2=250)
    log.info(f"The diped image is in: {dips_img}")
    log.info(f"The diped line is in: {dips_line}")
    log.info(f"The diped hist is in: {dips_hist}")
    # 绘图
    dip.get_cmp_plot(init_img, init_line, init_hist,
                     dips_img, dips_line, dips_hist,
                     i_im="Initial Image", i_li="Intial Contrast", i_hi="Initial Gray Scale",
                     d_im="Diped Image", d_li="Diped Contrast", d_hi="Diped Gray Scale")
    del dip

"""
first of all，先安装如下几个包：
-------------------------------------------------------------------------
    pip install --upgrade pip
    pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple
    pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
    pip install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
------------------------------------------------------------------------- 

0.刚进入软件的时候，先初始化x1, x2, y1, y2。
1.调用dip.DIP模块的时候，首先实例化一个图片对象，每张图片都是一个对象，需要指定图片的路径img_path，路径以“./pic/xxx”形式，需要指定输出图片的输出路径output_dir，
  如"data"，于是会在本地生成"./data/"目录，所有生成的图片都会写入到该目录下。实例化的时候，x1、x2、y1、y2可以不赋值，但建议第一次打开软件的时候，赋值为滑动条的当前值。
  
2.然后调用dip.is_exist()判断用户传进来的图片是否存在或找得到，若函数返回False, 则说明该模块不能识别图片路径，因此软件应该给予弹框等提提示用户找不到文件。

3.当第2步返回True时，软件才可调用 dip.get_init_img()以获得初始图片的背景图、对比度折线图及RGB灰度直方图的路径，软件便根据该路径找到该图片并展示出来。

4.用户通过拖动滑动条以获得x1, x2, y1, y2的值，此处建议增加一个确定按钮，用来提交这4个值给已经实例化的dip对象的方法dip.get_dips_img()以获得初始图片的背景图、
  对比度折线图及RGB灰度直方图的路径，软件便根据该路径找到该图片并展示出来。在该方法未返回参数前，软件应增加一个等待的进度条或转圈的交互动画，并且冻结所有按钮（即此时所有按钮为disabled），
  并设置超时时间，如time.sleep(15)，即15秒后若函数仍未返回则终止该函数的执行，并提示用户软件出错。（同样第2步也需要增加等待和超时的功能）。
  
5.若用户重新加载新的图片，则需要销毁前一个图片对象，才可重新实例化新的图片对象，即:
-------------------------------------------------------------------------
    del dip
    dip = DIP(img_path="./pic/xxx", output_dir="data", x1=20, x2=140, y1=100, y2=150) # x1-y2可不写，但是建议传上次的值进来
    # dip = DIP(img_path="./pic/xxx", output_dir="data") # 不传x1-y2亦可
-------------------------------------------------------------------------

6.正式开发或使用过程中请注释掉有关log模块的代码，以避免不必要的报错，此处引入仅仅为了DEBUG时打印更美观，但该模块是非必要的。
"""
