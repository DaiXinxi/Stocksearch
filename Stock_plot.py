# Description:#  这是一个批量绘制图片，滚动播放，并自动保存的程序。输入一个需要绘制的股票列表stocklist.xlsx。对于图片的格式要求可以进行相应的调整。
# Author:Dai Xinxi
# Date: 2020年2月25日

from threading import Timer
import time
import matplotlib.pyplot as plt
import numpy as np
from math import pi
from numpy import cos, sin
import xlrd
import tushare as ts


def stock_plot(x, y, pic_name, plot_title):  # 定义一个plot图表并实现保存和关闭的函数。参数为x,y两个列表，pic_name是文件名，plot_title是表格标题。
    print("当前时间：%s" % time.ctime())
    plt.plot(x, y, 'b')
    # plt.axis('equal')
    # plt.axis('scaled')
    plt.title(plot_title)
    plt.savefig('{}Printed_on_{}.jpg'.format(pic_name, time.strftime("%Y-%m-%d", time.localtime())))  # 保存当前的plot图片
    plt.pause(0.5)  # 显示秒数，如果不加plt.close，则如果继续画下一个plot，则原来的画布和图线还在。
    time.sleep(0.5)  # 延时0.5秒
    plt.close()  # 用了close之后，画布会被关闭，如果没有close，则会在原来的曲线上继续叠加后续的曲线。
    #global  t,i, j,count
    #count += 1
    #a=np.arange(0,np.pi)
    #b=[2,3,4]
    #fig1 = plt.figure(1)
    #plt.plot(a,b)
    #plt.show()
    '''plot data margin'''  # 用圆的参数方程画圆
    #angles_circle = [i * pi / 180 for i in range(0, 360)]  # i先转换成double
    #x = j*cos(angles_circle)
    #y = j*sin(angles_circle)
    #plt.plot(x, y, 'b')
    #plt.axis('equal')
    #plt.axis('scaled')
    #plt.savefig('{}test.jpg'.format(j))  # 保存当前的plot图片
    #plt.pause(1)  # 显示秒数，如果不加plt.close，则如果继续画下一个plot，则原来的画布和图线还在。
    #time.sleep(5)
    #plt.close()  # 用了close之后，画布会被关闭
    # 如果count小于10，开始下一次调度


#j=1
#count = 0
#if __name__ == '__main__':
#    while True:
#        # t = Timer(1, print_time)
#        # t.start()
#        print_time()
#        time.sleep(1)  # 暂停几秒钟
#        count += 1
#        j += 0.2
# 指定1秒后执行print_time函数

if __name__ == '__main__':
    filename = 'picked_stock_list.xls'
    stock_file = xlrd.open_workbook(filename)  # 打开需要绘制的股票的excel表
    sheet = stock_file.sheet_by_index(0)
    sheet_row_num = sheet.nrows
    for i in range(0, sheet_row_num):  # 依次读取每一行的数据
        # stock_number = str(sheet.cell_value(i, 0)).rstrip('.0')  # 用这种方式容易把类似于000030这种数字变成00003
        stock_number = str(sheet.cell_value(i, 0))[0:6]  # 用这种方式来取前六位，不容易出错。
        print(stock_number)  # 调试用
        today_date = time.strftime("%Y-%m-%d", time.localtime())
        # print(today_date)
        stock_k_data = ts.get_k_data(stock_number, start='2018-01-01', end=today_date)  # 获取股票K线数据
        stock_price = stock_k_data['close']  # 提取K线中的收盘价
        stock_date = stock_k_data['date']  # 取出时间列表
        # print(type(stock_price))
        stock_x_label = range(len(stock_price))  # 以列表长度建立列表，作为横坐标
        try:  # 因为用[-1]来取一个序列的最后一位数经常报错，所以用一个错误弹出的方法来避免报错。
            pic_title = '{}to{}'.format(stock_date[0], stock_date[-1])
        except KeyError:
            pic_title = '{}to{}'.format(stock_date[0], today_date)
        stock_plot(stock_x_label,  stock_price, stock_number, pic_title)  # 调用函数


